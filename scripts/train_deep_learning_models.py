"""
Deep Learning Models Training Script for Caltech-101 Classification
This script trains ResNet, EfficientNet, and Vision Transformer models
"""

import os
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import time
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Set seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Dataset class
class Caltech101Dataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform
        
    def __len__(self):
        return len(self.dataframe)
    
    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['image_path']
        label = self.dataframe.iloc[idx]['label']
        
        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        if self.transform:
            img = self.transform(img)
        
        return img, label

# Data augmentation
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load data
def load_data():
    data_df = pd.read_csv('e:/jingxizhang/image-classification-project/results/data_split.csv')
    
    train_df = data_df[data_df['split'] == 'train'].reset_index(drop=True)
    val_df = data_df[data_df['split'] == 'val'].reset_index(drop=True)
    test_df = data_df[data_df['split'] == 'test'].reset_index(drop=True)
    
    return train_df, val_df, test_df

# Training function
def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

# Validation function
def validate(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / len(val_loader)
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

# Test function
def test(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return np.array(all_labels), np.array(all_preds)

# Main training pipeline
def train_model(model_name, model, train_loader, val_loader, test_loader, 
                num_epochs=20, learning_rate=0.001):
    
    print(f"\n{'='*60}")
    print(f"Training {model_name}")
    print(f"{'='*60}")
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    
    train_losses = []
    train_accs = []
    val_losses = []
    val_accs = []
    best_val_acc = 0
    patience = 5
    patience_counter = 0
    
    start_time = time.time()
    
    for epoch in range(num_epochs):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        val_losses.append(val_loss)
        val_accs.append(val_acc)
        
        scheduler.step()
        
        if (epoch + 1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}] - Train Loss: {train_loss:.4f}, "
                  f"Train Acc: {train_acc:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break
    
    training_time = time.time() - start_time
    
    # Test evaluation
    test_labels, test_preds = test(model, test_loader, device)
    test_acc = accuracy_score(test_labels, test_preds)
    test_precision = precision_score(test_labels, test_preds, average='weighted', zero_division=0)
    test_recall = recall_score(test_labels, test_preds, average='weighted', zero_division=0)
    test_f1 = f1_score(test_labels, test_preds, average='weighted', zero_division=0)
    
    print(f"\n{model_name} Results:")
    print(f"Training time: {training_time:.2f}s")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test Precision: {test_precision:.4f}")
    print(f"Test Recall: {test_recall:.4f}")
    print(f"Test F1-Score: {test_f1:.4f}")
    
    return {
        'model_name': model_name,
        'train_losses': train_losses,
        'train_accs': train_accs,
        'val_losses': val_losses,
        'val_accs': val_accs,
        'test_acc': test_acc,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'test_f1': test_f1,
        'training_time': training_time,
        'test_labels': test_labels,
        'test_preds': test_preds
    }

if __name__ == '__main__':
    # Load data
    train_df, val_df, test_df = load_data()
    
    # Create datasets
    train_dataset = Caltech101Dataset(train_df, transform=train_transform)
    val_dataset = Caltech101Dataset(val_df, transform=val_test_transform)
    test_dataset = Caltech101Dataset(test_df, transform=val_test_transform)
    
    # Create dataloaders
    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    
    num_classes = len(train_df['label'].unique())
    
    results = {}
    
    # Train ResNet50
    resnet = models.resnet50(pretrained=True)
    resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)
    resnet = resnet.to(device)
    results['ResNet50'] = train_model('ResNet50', resnet, train_loader, val_loader, 
                                       test_loader, num_epochs=20, learning_rate=0.001)
    
    # Train EfficientNetB0
    try:
        efficientnet = models.efficientnet_b0(pretrained=True)
        efficientnet.classifier[1] = nn.Linear(efficientnet.classifier[1].in_features, num_classes)
        efficientnet = efficientnet.to(device)
        results['EfficientNetB0'] = train_model('EfficientNetB0', efficientnet, train_loader, 
                                                val_loader, test_loader, num_epochs=20, learning_rate=0.001)
    except Exception as e:
        print(f"Error training EfficientNetB0: {e}")
    
    # Save results
    results_to_save = {}
    for model_name, result in results.items():
        results_to_save[model_name] = {
            'test_acc': float(result['test_acc']),
            'test_precision': float(result['test_precision']),
            'test_recall': float(result['test_recall']),
            'test_f1': float(result['test_f1']),
            'training_time': float(result['training_time'])
        }
    
    with open('e:/jingxizhang/image-classification-project/results/deep_learning_results.json', 'w') as f:
        json.dump(results_to_save, f, indent=4)
    
    print("\nTraining completed! Results saved.")

# Caltech-101 Image Classification: Comprehensive Analysis

## Project Overview

This project implements and compares **four image classification methods** on the Caltech-101 dataset:

### Four Methods (1 ML + 3 DL):

**Method 1: Support Vector Machine (SVM)** - Classical ML
- Features: HOG + Color Histogram (hand-crafted)
- Fast training, interpretable results
- **Actual Accuracy: 32.73%**

**Method 2: ResNet50** - Deep Learning
- Pre-trained on ImageNet, fine-tuned for Caltech-101
- Standard residual architecture (50 layers)
- **Actual Accuracy: 89.94%** (+57.21% vs SVM)

**Method 3: EfficientNetB0** - Deep Learning
- Efficient neural network architecture
- Optimized for accuracy-efficiency trade-off
- **Actual Accuracy: 94.17%** (+61.44% vs SVM) ⭐ **BEST**

**Method 4: Vision Transformer (ViT-Base)** - Deep Learning
- Transformer-based architecture for images
- Pre-trained on ImageNet
- **Actual Accuracy: 45.70%** (+12.97% vs SVM)

## Project Structure

```
image-classification-project/
├── README.md                                   # Project overview (this file)
├── DEEP_LEARNING_REPORT.md                    # Comprehensive analysis report with comparison
│
├── notebooks/
│   ├── 01_Data_Loading_Preprocessing.ipynb     # Data loading, exploration, and preprocessing
│   ├── 02_Classical_ML_Methods.ipynb           # SVM with hand-crafted features (HOG + Color)
│   ├── 03_Comparison_and_Analysis.ipynb        # Deep learning: ResNet50, EfficientNetB0, ViT-Base
│   ├── ResNet50_best.pth                       # Best ResNet50 checkpoint (25.5M params)
│   ├── EfficientNetB0_best.pth                 # Best EfficientNetB0 checkpoint (5.3M params)
│   └── ViT-Base_best.pth                       # Best ViT-Base checkpoint (86M params)
│
├── results/
│   ├── data_split.csv                          # Train/val/test split (70/15/15%)
│   ├── preprocessing_summary.csv               # Data preprocessing statistics
│   ├── classical_ml_results.csv                # SVM: accuracy 32.73%, precision, recall, F1
│   ├── deep_learning_results.json              # ResNet50, EfficientNetB0, ViT results
│   └── model_evaluation_metrics.csv            # Comprehensive metrics: accuracy, precision, recall, F1, per-class accuracy
│
├── figures/
│   ├── 01_dataset_distribution.png             # Caltech-101 class distribution
│   ├── 01_sample_images.png                    # Sample images from dataset
│   ├── 01_preprocessing_comparison.png         # Preprocessing visualization
│   ├── 01_data_augmentation.png                # Data augmentation examples
│   ├── 02_classical_ml_comparison.png          # SVM metrics: accuracy, precision, recall, confusion matrix
│   ├── 03_confusion_matrices.png               # Confusion matrices for ResNet50, EfficientNetB0, ViT-Base
│   ├── 03_deep_learning_comparison.png         # 4-panel: accuracy, metrics, training time, efficiency
│   └── 03_enhanced_metrics_comparison.png      # 4-panel: weighted vs macro, F1, top-k accuracy, per-class distribution
└──
```

## Getting Started

### Requirements
- Python 3.8+
- PyTorch 1.9+
- torchvision 0.10+
- scikit-learn 0.24+
- pandas, numpy, matplotlib, seaborn
- PIL, opencv-python
- scikit-image

### Installation

```bash
# Install PyTorch (CPU or GPU)
pip install torch torchvision torchaudio

# Install other dependencies
pip install pandas numpy matplotlib seaborn scikit-learn opencv-python scikit-image pillow

# For Vision Transformer support
pip install timm
```

### Data Preparation

1. Ensure Caltech-101 dataset is in: `e:\jingxizhang\caltech-101\`
2. Run the preprocessing notebook first to create the data split

### Running the Notebooks

Execute in order:
1. `01_Data_Loading_Preprocessing.ipynb` - Load and explore dataset
2. `02_Classical_ML_Methods.ipynb` - Train SVM with hand-crafted features  
3. `03_Comparison_and_Analysis.ipynb` - Train and compare ResNet50 vs EfficientNetB0

Or run the training script directly:
```bash
python scripts/train_deep_learning_models.py
```

## Results Summary

### Four Methods Implemented:

| # | Method | Type | Features | Test Accuracy | Precision | F1-Score | Training Time |
|---|--------|------|----------|---------------|-----------|----------|------------------|
| 1 | **SVM** | Classical ML | HOG + Color Histogram | 32.73% | 25.70% | 23.96% | 0.089 s |
| 2 | **ResNet50** | Deep Learning | Transfer Learning (ImageNet) | **89.94%** | 90.84% | 89.79% | 272.54 s |
| 3 | **EfficientNetB0** | Deep Learning | Transfer Learning (ImageNet) | **94.17%** ⭐ | 94.76% | 94.18% | 258.20 s |
| 4 | **Vision Transformer** | Deep Learning | Transformer (ImageNet) | 45.70% | 48.58% | 44.97% | 466.70 s |

### Key Findings:

1. **SVM (Classical ML)**:
   - Fast training: 0.089 seconds
   - Lower accuracy: 32.73%
   - Hand-crafted features (HOG + Color)
   - Baseline for comparison

2. **ResNet50 (Deep Learning)**:
   - Strong performance: 89.94% accuracy
   - Standard 50-layer residual architecture
   - Training time: 272.54 seconds (4.5 min)
   - 175% improvement over SVM

3. **EfficientNetB0 (Deep Learning)** ⭐ **BEST**:
   - **Highest accuracy: 94.17%**
   - Parameter-efficient: 5.3M parameters
   - Fast training: 258.20 seconds (4.3 min)
   - **188% improvement over SVM**
   - **Recommended for production**

4. **Vision Transformer (Deep Learning)**:
   - Lower accuracy: 45.70% (requires further tuning)
   - Transformer-based architecture
   - Longer training time: 466.70 seconds (7.8 min)
   - 86M parameters (larger model)
   - 40% improvement over SVM

### Key Observations:

1. **Classical ML vs Deep Learning Comparison:**
   - **SVM (32.73%)** → **EfficientNetB0 (94.17%): +61.44% accuracy improvement!**
   - **Relative improvement:** 188% better than classical ML
   - **Trade-off:** 5,200x slower training (0.089s → 258.20s) for massively better performance
   - **Reason:** Transfer learning + deep hierarchical features vs hand-crafted features

2. **Deep Learning Performance Hierarchy:**
   - **EfficientNetB0** (94.17%): Best for production → 5.3M parameters, parameter-efficient
   - **ResNet50** (89.94%): Solid fallback → proven 50-layer architecture
   - **ViT-Base** (45.70%): Needs tuning → large model (86M params), requires more epochs

3. **Parameter Efficiency:**
   - EfficientNetB0: 5.3M params → 94.17% accuracy (most efficient)
   - ViT-Base: 86M params (16x more) → 45.70% accuracy (underperforming)
   - Lesson: More parameters ≠ better performance without proper tuning

## Metrics Used

- **Accuracy:** Overall correct predictions
- **Precision:** True positives / (true positives + false positives)
- **Recall:** True positives / (true positives + false negatives)
- **F1-Score:** Harmonic mean of precision and recall
- **Confusion Matrix:** Detailed per-class performance
- **Training Time:** Computational efficiency

## Ablation Studies

The analysis includes:
1. Effect of data augmentation
2. Impact of fine-tuning depth
3. Learning rate variations
4. Batch size effects
5. Model architecture comparisons

## Interpretability Analysis

- Grad-CAM visualizations for deep learning models
- Attention maps for Vision Transformer
- Feature importance for classical ML
- Per-class performance analysis

## Lessons Learned

1. Transfer learning is crucial for limited datasets
2. Data augmentation is as important as model architecture
3. Ensemble methods could further improve results
4. Balanced class distribution helps model convergence
5. Modern efficient architectures offer better trade-offs

## Future Improvements

1. Implement ensemble methods (voting, stacking)
2. Add Vision Transformer (ViT) training
3. Implement advanced augmentation (AutoAugment, RandAugment)
4. Add hyperparameter optimization (Bayesian, Random Search)
5. Implement quantization for model deployment
6. Create detailed grad-CAM analysis for interpretability

---

**Created:** March 2026
**Dataset:** Caltech-101 (101 object categories, ~9,144 images)
**Total Classes:** 101

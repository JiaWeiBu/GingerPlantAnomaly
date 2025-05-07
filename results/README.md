# Results

[Back to Main README](../README.md)

## Table of Contents
- [Overview](#overview)
- [Model Analysis](#model-analysis)
  - [STFPM – Best Overall Performer](#stfpm--best-overall-performer)
  - [PatchCore – Strong Precision, Slight Recall Limitations](#patchcore--strong-precision-slight-recall-limitations)
  - [Reverse Distillation – Balanced and Promising](#reverse-distillation--balanced-and-promising)
  - [FastFlow – Decent Generalist, Lacking Sensitivity](#fastflow--decent-generalist-lacking-sensitivity)
  - [CFlow – Least Reliable Overall](#cflow--least-reliable-overall)
- [Week 3 Visual Evaluation](#week-3-visual-evaluation)
- [Week 8 Visual Evaluation](#week-8-visual-evaluation)
- [Week 12 Visual Evaluation](#week-12-visual-evaluation)
- [Week 18 Visual Evaluation](#week-18-visual-evaluation)
- [Performance Overview](#performance-overview)
  - [Average Performance](#average-performance)
  - [Accuracy Metrics](#accuracy-metrics)
    - [Overall Accuracy](#overall-accuracy)
    - [Weekly Accuracy](#weekly-accuracy)
      - [Week 3](#week-3)
      - [Week 8](#week-8)
      - [Week 12](#week-12)
      - [Week 18](#week-18)
- [Detailed Results](#detailed-results)
  - [Metrics Table](#metrics-table)

## Overview
The results of the anomaly detection models are stored in the `results/` directory. This includes evaluation metrics, plots, and saved models. [Refer to the generated plots and metrics for detailed insights.](./result.xlsx)

## Model Analysis
### STFPM – Best Overall Performer
**Strengths:**
- Highest average accuracy (86.22%) and best F1 score (84.03%), showing a strong balance between precision and recall.
- Excellent at localizing anomalies, particularly in dying and contrast variation scenarios.
- High specificity (98.75%) and very low false positive rate (1.25%), meaning it rarely misclassifies healthy plants.
- Best performer in hue-down 30%, a previously difficult category for all models.

**Weaknesses:**
- Slight sensitivity to minor hue shifts (15%), occasionally flagging healthy images.
- May require tuning of sensitivity thresholds to prevent false alarms in borderline cases.

### PatchCore – Strong Precision, Slight Recall Limitations
**Strengths:**
- Perfect precision (100%) and specificity (100%), meaning it only flags anomalies when it is very sure.
- Excellent in detecting dying conditions, particularly in “dying 2” and “dying 3”.
- Ideal for applications that require minimal false positives.

**Weaknesses:**
- Moderate recall (63.63%), indicating it sometimes misses subtle anomalies.
- Underperformed slightly in hue-down scenarios, where sensitivity was not high enough to cross anomaly thresholds.
- May benefit from greater sensitivity in early-stage or subtle color changes.

### Reverse Distillation – Balanced and Promising
**Strengths:**
- Consistently strong across many conditions, especially in contrast variations and dying 3.
- Good recall (64.58%) and F1 score (73.71%), indicating a balance between sensitivity and precision.
- Excellent at detecting structural abnormalities and discoloration, including root shape anomalies.

**Weaknesses:**
- Slight tendency to flag normal plant structures as anomalies, such as triangular roots, possibly due to limited diversity in training data.
- High variability in performance depending on visual input complexity.

### FastFlow – Decent Generalist, Lacking Sensitivity
**Strengths:**
- High precision (87.39%) and specificity (90.67%), indicating a good ability to avoid false positives.
- Performs well in normal conditions and under mild contrast variations.

**Weaknesses:**
- Low recall (56.31%) and limited sensitivity to subtle anomalies like early discoloration or mild dying.
- Poor performance in hue-down conditions, especially at 15%.
- Often detects the anomaly regions visually but fails to surpass detection thresholds.

### CFlow – Least Reliable Overall
**Strengths:**
- Performs acceptably on normal samples (74.90% accuracy), often generating clean maps with minimal false positives.
- Good at indicating normalcy rather than flagging anomalies, making it suitable as a baseline validator.

**Weaknesses:**
- Lowest performance across nearly all metrics, including recall (29.90%), F1 score (37.65%), and AUROC (45.50%).
- Poor sensitivity to hue-down and dying samples, often failing to flag visible anomalies.
- May lack robustness against color-based transformations or require better threshold tuning.

### Week 3 Visual Evaluation
The Week 3 visual evaluation step was insightful regarding the response of each model to normal and anomalous visual cues, especially when viewed at full crop resolution. Anomaly predictions were overlaid on the test images in this step, and qualitative observations were recorded on how well the predictions aligned with the actual plant conditions.

#### Model Observations
- **CFlow**:  
  CFlow showed consistent alignment with normal samples, often producing clean prediction masks with little or no false positives. However, its behavior on anomaly images—particularly under hue shift and dying leaf simulations—was difficult to interpret. In many cases, the model neither indicated anomalies with confidence nor showed strong heatmap hints. This raises concerns about whether it is responding appropriately or simply not registering subtle changes.

- **FastFlow**:  
  FastFlow performed adequately on both good and bad cases. On normal samples and contrast changes, it maintained acceptable prediction clarity. However, on bad samples, the model had limited sensitivity. Visual cues like browning or color changes were not strongly suggested, reflecting a lack of discriminative power for mild anomaly transformations.

- **PatchCore**:  
  PatchCore followed a similar trend to FastFlow, with good performance on normal images and tolerably medium performance on bad ones. On dying variation and hue-down cases, it weakly indicated problematic areas but often failed to cross the anomaly threshold. Like FastFlow, it appeared to sense something was wrong but lacked the confidence to explicitly classify it as an anomaly.

- **Reverse Distillation**:  
  Reverse Distillation showed slight variability in detecting early discoloration and yellowing, even in "good" images. While this points to sensitivity, it can lead to false positives on borderline cases. In anomalous cases, especially with dying variants, the model was capable of detecting affected regions but could benefit from further tuning to amplify anomaly signal strength. Its performance suggests a strong underlying ability, but the threshold requires refinement.

- **STFPM**:  
  STFPM was the most stable in terms of visual feedback. It accurately differentiated normal and abnormal samples and consistently emphasized affected areas under hue-down and dying conditions. However, its performance on hue-down 15% variation cases was somewhat concerning, as it tended to label minor hue changes as anomalies even when these were within acceptable visual limits for healthy plants. Nonetheless, among all models, STFPM had the best localization and confidence on visual anomaly maps.

#### General Observations
Of all the models, hue-down changes were the hardest to evaluate. These sorts of changes consistently produced anomaly flags on both "good" and "bad" samples, obscuring the models' ability to identify subtle changes in coloration. This highlights the need for either more complex hue-sensitive augmentation processing or refined thresholding logic.

The Week 3 visual evaluation accentuates both the strengths and weaknesses of the models. It confirms the necessity for continued human-in-the-loop validation, especially where model outputs are responsive to uncertain color or contrast variations in real-world plant images.

#### Summary
The Week 3 visual evaluation indicates that while all models possessed a baseline ability to delineate normal from anomalous plant conditions, they exhibited variable sensitivity and accuracy:
- **CFlow**: Performed well under normal samples but struggled to make definitive outputs on anomalous ones, raising concerns about its reliability under subtle disturbances.
- **FastFlow** and **PatchCore**: Largely consistent but lacked the depth to pick up on less obvious signs of stress, such as early color shifts.
- **Reverse Distillation**: Yielded good discoloration and shadow-based anomaly detection with high potential, though it bordered on being too sensitive in some good samples.
- **STFPM**: Most consistent, with well-localized and sharp detections, offering a good trade-off between sensitivity and specificity.

Hue-down transformations exposed a blind spot common to all models, which tended to confuse even visually healthy images. These results highlight the importance of tailored preprocessing and postprocessing methods, particularly for ambiguous or color-based anomaly cues in plant health monitoring.

### Week 8 Visual Evaluation
Week 8 visual evaluation provided deeper insight into how effective each model had been in coping with increasing dataset complexity and higher plant condition variability. With increasing use of full crop resolution for testing, models were assessed on the basis of their ability to accurately localize anomalies and avoid false detections, particularly as increasingly variable contrast and hue changes were included.

#### Model Observations
- **CFlow**:  
  CFlow performed well on normal samples, often generating clean masks without mistakenly labeling the background. However, its performance on bad samples was still inconsistent. The model did not conclusively react to many visually apparent anomalies, especially under slight hue variations or progressive plant rot. Though its low sensitivity might restrict false positives, it also raised questions about its general detection confidence and reliability.

- **FastFlow**:  
  FastFlow demonstrated better robustness on normal samples, perhaps due to improved background handling and fine-tuning in prediction confidence. Its anomaly detection on bad images was slightly improved, with clearer heatmaps around affected areas. However, subtle changes such as early-stage decay or slight hue downshifts continued to be underrepresented. The model appeared to need stronger anomaly triggers to confidently classify an image as abnormal.

- **PatchCore**:  
  PatchCore was especially strong in handling both normal and anomaly images. It performed excellent discrimination on normal examples without requiring explicit background filtering. Under anomaly instances, particularly with subtle variations, the model produced logical heatmap activations. While it sometimes failed to cross anomaly thresholds on more subtle cases, its localization remained consistent with actual areas of interest, making it a reliable middle-ground candidate.

- **Reverse Distillation**:  
  Reverse Distillation further improved its interpretability by clearly showing abnormal regions, even in complex plant geometries. It handled dying and hue-shifted variants more firmly than it had in Week 3 and managed to differentiate between normal and suspect plant conditions. Its sensitivity also allowed it to detect incipient discoloration and minute structural weaknesses. However, it still required slight calibration to reduce false positives from benign hue changes.

- **STFPM**:  
  STFPM performed better than all other models in terms of map distinctness and anomaly localization. It highly discriminated normal from poor samples, often yielding intricate and specific heatmaps even for very minor changes. Hue-down cases were well handled, though at the 15% threshold, some visual clues were borderline, leading to slight misclassifications. Nonetheless, STFPM still performed better with minimal misclassification and good spatial accuracy.

#### General Observations
Hue-down 15% was a recurring problem for all models. This change was subtle enough to be within normal limits but was able to mislead some models into marking them as anomalies. This highlights the importance of better anomaly thresholding logic and possibly rethinking whether such subtle hue changes should even be considered anomalies under field conditions.

#### Summary
Week 8 visual evaluation confirmed continued improvement in model stability and detection confidence, with almost all models demonstrating greater capability in responding to more sophisticated plant structures and denser leaf patterns:
- **CFlow**: Continued its excellence in precise predictions of normal samples but remained limited in decisiveness when subjected to subtle anomalies. Its indecision in discriminating minor visual impairments remained an ongoing shortcoming.
- **FastFlow**: Fared marginally better than in Week 3, with improved attention and reduced noise in predictions. However, it still lacked the depth for routine flagging of borderline anomalies, especially color-related changes.
- **PatchCore**: Achieved fair performance, particularly in "dying" changes where indications were strongly prominent. However, it exhibited some conservatism in considering gentle deviations as anomalies.
- **Reverse Distillation**: Demonstrated good visual acuteness, correctly identifying discolored and shadowed regions. However, its heightened sensitivity occasionally picked up non-critical differences, indicating that thresholding could be improved.
- **STFPM**: Once again outperformed the others, demonstrating excellent localization accuracy and robust anomaly detection—even in visually ambiguous cases. However, hue-down 15% transformations remained a problematic case, occasionally leading to false positives in healthy samples.

These results emphasize the importance of high color sensitivity calibration and validate STFPM's leadership as a prevailing model for accurate plant anomaly detection at this level of development.

### Week 12 Visual Evaluation
The Week 12 visual inspection step provides a mid-stage insight into how each anomaly detection model responded to ginger plants with moderate growth. The dataset for this week has varied images, which is a well-balanced mix of normal and abnormal conditions, along with simulated augmentations such as dying leaves, contrast changes, and hue shifts. The vegetation at this growth stage is denser and more developed than in Week 8, with greater shadow and texture complexity, offering subtle challenges to anomaly detection.

#### Model Observations
- **CFlow**:  
  CFlow provided a decent but sub-par performance on normal images. Its predictions were occasionally interrupted by background elements, and prediction masks were noisy. On anomalous images, especially in the dying or hue-down case, CFlow performed exceedingly poorly, producing indistinct or useless heatmaps. The model did not highlight critical areas numerous times or discern between minor visual noise vs. actual anomalies, an indication of insufficient sensitivity at this mid-stage growth.

- **FastFlow**:  
  FastFlow mimicked CFlow's performance with normal predictions moderately well aligned but disrupted by visual noise, possibly plant shadow or minor textural differences. On the anomaly samples, FastFlow was unstable and less convincing with faint heatmap signals on obvious cases like dying leaves. Its inability to flag anomalies confidently or localize them sharply reduces its practical utility without further tuning or refinement.

- **PatchCore**:  
  PatchCore, in contrast, performed exceptionally well, particularly on normal samples where its emphasis on small details made it impervious to background noise. Rather astonishingly, PatchCore detected plant shadows as anomalies, which, although technically incorrect, speaks volumes about its hypersensitivity visually. On dying samples and color changes, the model exhibited clear and confident detection, outperforming both CFlow and FastFlow by a long way.

- **Reverse Distillation**:  
  Reverse Distillation provided solid and stable performance in most test cases. On good images, it maintained low anomaly scores, even though background interference impacted its consistency to some extent. On bad samples, especially those with dying plant symptoms, the model possessed decent capability to highlight anomalous regions, but its responses lacked the consistency of PatchCore or STFPM. It was equivocal on hue-down at 15%, but at 30% it began to respond more emphatically, suggesting that its sensitivity curve is more commensurate with stronger visual changes.

- **STFPM**:  
  STFPM continued to be a leading performer. It maintained perfect alignment on normal samples with no false positives and exhibited excellent precision in identifying dying and highly altered plants. In hue-down tests, STFPM behaved as intended—it had negligible detection at 15% shifts but became effective at 30%, which means it has a well-calibrated sensitivity threshold. Among all models, STFPM offered the best localization accuracy and anomaly confidence combination.

#### General Observations
Across the board, hue-down changes remained difficult, particularly at the 15% level where changes were too subtle for some models to mark as anomalies with any certainty. Models like CFlow and FastFlow would miss these changes, while PatchCore and STFPM responded more reliably at larger hue changes. Visual clutter caused by background noise continued to be a challenge, particularly for CFlow and Reverse Distillation.

#### Summary
The Week 12 visual examination demonstrates an improved delineation between normal and abnormal plant conditions, with all models exhibiting varying degrees of consistency and finesse:
- **CFlow**: Performed modestly on good samples but lacked consistency, with a tendency to yield noisy or incomplete heatmaps on anomalous inputs.
- **FastFlow**: Exhibited similar performance—reasonably good for healthy plants but struggled with subtle anomalies, which resulted in ambiguous predictions.
- **PatchCore**: Was good at precise anomaly localization, especially on the dying leaf samples, but tended to mistake shadows for abnormalities due to its high sensitivity.
- **Reverse Distillation**: Performed very well on both good and defective images, though it was moderately troubled by background artifacts, meaning that it required improved context filtering.
- **STFPM**: Yielded the most consistent and visually accurate results, with correct identification of normal and anomalous regions and minimal false positives.

Hue-down transformations nonetheless remained difficult for all models, particularly at lower intensity shifts, reflecting a continued limitation for color-based anomaly detection. These findings highlight again the need for calibrated detection thresholds and more advanced handling of subtle color gradations to enhance reliability for plant health monitoring.

### Week 18 Visual Evaluation
Week 18 visual inspection presented a full challenge with the biggest image set so far, which had densely planted ginger crops lined up next to one another with minimal or no background distractions. This specific arrangement gave a cleaner environment for the detection of visual anomalies, allowing clearer analysis of model behavior under ideal conditions. Anomaly overlays were tested in full-resolution images, helping identify the strengths and weaknesses of each model.

#### Model Observations
- **CFlow**:  
  CFlow had unstable behavior. On well-behaved samples, it often produced streaky heatmaps with sparse false positives, reducing interpretability. Even when there was a clean background, the model struggled to maintain stability and tended to mark out non-anomalous regions. However, in dying and hue-down situations, while it could not produce robust anomaly masks, it rankably identified the regions correctly—i.e., it could be utilized as a validation layer, but not as a primary detector.

- **FastFlow**:  
  FastFlow delivered mean visual quality, particularly on normal samples where its output was acceptable despite numerous erroneous highlights. On dying and hue-down 30% samples, FastFlow was greatly improved, accurately highlighting regions of interest despite occasionally not extending to the anomaly boundary. However, a hue-down of 15% remained a soft spot, often not being highlighted. Overall, FastFlow's ability to localize anomalies made it visually comprehensible, but it lacked decisiveness about faint anomalies.

- **PatchCore**:  
  PatchCore performed exceptionally well, especially on anomaly samples. It detected all dying symptoms confidently and generated consistent heatmaps with good localization. On normal samples, the model flagged some residual pot structures as anomalies, but successful filtering reduced most such false alarms. Its sensitivity was very useful in dying and hue-down testing. Despite some low-level misclassifications, PatchCore was one of the most dependable detectors for Week 18.

- **Reverse Distillation**:  
  Reverse Distillation was very sensitive, detecting both plant roots and subtle color changes. Interestingly, it tended to flag triangular root growth patterns as anomalies, which are likely normal variations not well represented in the training data. On dead samples, even when detection scores were below the threshold, the anomaly regions were flagged—suggesting that with threshold tuning, performance could be significantly improved. Hue-down performance at 15% remained poor, but detection on structurally different features like roots was always robust.

- **STFPM**:  
  STFPM was still the most visually accurate model. On normal samples, it had no qualms about producing clean, blank masks. For dying leaves, it ranked anomaly regions with high confidence correctly, even for samples that technically failed detection thresholds. Hue-down 15% changes caused score reductions, but the anomaly regions were still distinctly highlighted, confirming STFPM's localization capability. At 30%, detection became much clearer. Its ability to consistently favor correct areas, even under slight changes, makes STFPM the strongest and most consistent model visually.

#### General Observations
In general, the Week 18 dataset (high size and low background noise) facilitated a purer test of anomaly detection performance. Highly context-dependent background models (e.g., CFlow) did not work well, whereas highly internally consistent models (PatchCore, STFPM) worked well. Hue-down transformations remained difficult for most models at 15%, though higher variation levels improved interpretability. Visual intuition this week decidedly supports the use of STFPM and PatchCore in real-world applications, especially where accurate localization and low background interference are a top priority.

#### Summary
The Week 18 visual testing illustrates strong model robustness growth, especially against the high image count of the dataset and low background noise by highly dense plant stands:
- **CFlow**: Exhibited basic performance on shared samples but remained behind in anomaly cases with scant visual cues, even when they contained blatant defects.
- **FastFlow**: Had decent consistency, accurately localizing bad sample errors, but also provided some bad classifications on good samples, showing ongoing sensitivity limitations.
- **PatchCore**: Had strong overall performance, particularly in dead leaf detection and rejecting irrelevant pot-based outliers, and is rated as one of the better-performing models this week.
- **Reverse Distillation**: Performed well, especially where root abnormalities occurred in plants, although it tended to incorrectly flag normal root shapes as abnormal on occasion due to lack of exposure during training.
- **STFPM**: Again performed exceptionally well, correctly identifying gross and fine abnormalities, and even when detection failed, it still produced high anomaly scores for the right regions.

While hue-down conversions, especially at 15%, remained a weak link for all models, the more explicit visual organization of Week 18 images further exposed each model's detection rationale. These findings reinforce the need for clean input data and continue to emphasize the need for diverse training samples and higher model sensitivity to tiny color and structural changes.

## Performance Overview
### Average Performance
| Model                | Accuracy | Precision | Recall | F1 Score | Specificity | False Positive Rate | False Negative Rate | Balanced Accuracy | Youden's Index (J) | Negative Predictive Value | AUROC  | AUPR   |
|----------------------|----------|-----------|--------|----------|-------------|----------------------|----------------------|-------------------|--------------------|--------------------------|--------|--------|
| **CFlow**            | 51.04%  | 55.62%    | 29.90% | 37.65%   | 72.19%      | 27.81%               | 70.10%               | 51.04%            | 2.09%              | 49.96%                  | 45.50% | 69.26% |
| **FastFlow**         | 73.49%  | 87.39%    | 56.31% | 67.75%   | 90.67%      | 9.33%                | 43.69%               | 73.49%            | 46.98%             | 67.66%                  | 78.86% | 79.95% |
| **PatchCore**        | 81.81%  | 100.00%   | 63.63% | 76.94%   | 100.00%     | 0.00%                | 36.37%               | 81.81%            | 63.63%             | 74.06%                  | 82.75% | 84.29% |
| **Reverse Distillation** | 77.55% | 87.38% | 64.58% | 73.71%   | 90.79%      | 9.21%                | 35.42%               | 77.68%            | 55.36%             | 72.36%                  | 81.06% | 81.83% |
| **STFPM**            | 86.22%  | 98.08%    | 73.86% | 84.03%   | 98.75%      | 1.25%                | 26.14%               | 86.30%            | 72.61%             | 79.28%                  | 82.63% | 80.89% |

### Accuracy Metrics
#### Overall Accuracy
| Variable            | Model                | Accuracy |
|---------------------|----------------------|----------|
| **Normal**          | **CFlow**            | 74.90%   |
|                     | **FastFlow**         | 87.92%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 93.06% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.7** | **CFlow**          | 65.97%   |
|                     | **FastFlow**         | 93.65%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 92.36% |
|                     | **STFPM**            | 93.75%   |
| **Contrast Down 0.9** | **CFlow**          | 78.33%   |
|                     | **FastFlow**         | 91.67%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 96.67% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.1** | **CFlow**            | 71.88%   |
|                     | **FastFlow**         | 90.93%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 85.42% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.3** | **CFlow**            | 71.67%   |
|                     | **FastFlow**         | 86.25%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 87.24% |
|                     | **STFPM**            | 100.00%  |
| **Dying 1**         | **CFlow**            | 47.53%   |
|                     | **FastFlow**         | 70.09%   |
|                     | **PatchCore**        | 83.01%   |
|                     | **Reverse Distillation** | 78.72% |
|                     | **STFPM**            | 74.11%   |
| **Dying 2**         | **CFlow**            | 22.44%   |
|                     | **FastFlow**         | 84.74%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 72.92% |
|                     | **STFPM**            | 95.64%   |
| **Dying 3**         | **CFlow**            | 33.19%   |
|                     | **FastFlow**         | 87.64%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 91.67% |
|                     | **STFPM**            | 100.00%  |
| **Hue Down 15**     | **CFlow**            | 19.98%   |
|                     | **FastFlow**         | 24.30%   |
|                     | **PatchCore**        | 18.53%   |
|                     | **Reverse Distillation** | 29.13% |
|                     | **STFPM**            | 29.18%   |
| **Hue Down 30**     | **CFlow**            | 25.00%   |
|                     | **FastFlow**         | 38.13%   |
|                     | **PatchCore**        | 42.50%   |
|                     | **Reverse Distillation** | 51.70% |
|                     | **STFPM**            | 79.39%   |

#### Weekly Accuracy
##### Week 3
| Variable            | Model                | Accuracy |
|---------------------|----------------------|----------|
| **Normal**          | **CFlow**            | 83.33%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 83.33% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.7** | **CFlow**          | 75.00%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 75.00%   |
| **Contrast Down 0.9** | **CFlow**          | 100.00%  |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.1** | **CFlow**            | 75.00%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 75.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.3** | **CFlow**            | 66.67%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 66.67% |
|                     | **STFPM**            | 100.00%  |
| **Dying 1**         | **CFlow**            | 100.00%  |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 75.00%   |
|                     | **Reverse Distillation** | 75.00% |
|                     | **STFPM**            | 50.00%  |
| **Dying 2**         | **CFlow**            | 0.00%    |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 0.00%  |
|                     | **STFPM**            | 100.00%  |
| **Dying 3**         | **CFlow**            | 33.33%   |
|                     | **FastFlow**         | 66.67%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 66.67% |
|                     | **STFPM**            | 100.00%  |
| **Hue Down 15**     | **CFlow**            | 16.67%   |
|                     | **FastFlow**         | 0.00%    |
|                     | **PatchCore**        | 0.00%    |
|                     | **Reverse Distillation** | 0.33%  |
|                     | **STFPM**            | 0.00%    |
| **Hue Down 30**     | **CFlow**            | 20.00%   |
|                     | **FastFlow**         | 20.00%   |
|                     | **PatchCore**        | 20.00%   |
|                     | **Reverse Distillation** | 33.33% |
|                     | **STFPM**            | 0.83%    |

##### Week 8
| Variable            | Model                | Accuracy |
|---------------------|----------------------|----------|
| **Normal**          | **CFlow**            | 100.00%  |
|                     | **FastFlow**         | 91.67%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.7** | **CFlow**          | 78.57%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.9** | **CFlow**          | 100.00%  |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.1** | **CFlow**            | 81.82%   |
|                     | **FastFlow**         | 90.91%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.3** | **CFlow**            | 100.00%  |
|                     | **FastFlow**         | 80.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 92.31% |
|                     | **STFPM**            | 100.00%  |
| **Dying 1**         | **CFlow**            | 27.27%   |
|                     | **FastFlow**         | 72.73%   |
|                     | **PatchCore**        | 81.82%   |
|                     | **Reverse Distillation** | 87.50% |
|                     | **STFPM**            | 75.00%  |
| **Dying 2**         | **CFlow**            | 30.00%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 91.67% |
|                     | **STFPM**            | 91.67%  |
| **Dying 3**         | **CFlow**            | 11.11%   |
|                     | **FastFlow**         | 88.89%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Hue Down 15**     | **CFlow**            | 30.77%   |
|                     | **FastFlow**         | 38.46%   |
|                     | **PatchCore**        | 15.38%   |
|                     | **Reverse Distillation** | 18.18% |
|                     | **STFPM**            | 0.45%   |
| **Hue Down 30**     | **CFlow**            | 20.00%   |
|                     | **FastFlow**         | 0.00%    |
|                     | **PatchCore**        | 30.00%   |
|                     | **Reverse Distillation** | 38.46% |
|                     | **STFPM**            | 0.69%   |

##### Week 12
| Variable            | Model                | Accuracy |
|---------------------|----------------------|----------|
| **Normal**          | **CFlow**            | 60.00%   |
|                     | **FastFlow**         | 60.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 88.89% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.7** | **CFlow**          | 71.43%   |
|                     | **FastFlow**         | 85.71%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 75.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.9** | **CFlow**          | 80.00%   |
|                     | **FastFlow**         | 80.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.1** | **CFlow**            | 83.33%   |
|                     | **FastFlow**         | 83.33%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 66.67% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.3** | **CFlow**            | 80.00%   |
|                     | **FastFlow**         | 80.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Dying 1**         | **CFlow**            | 20.00%   |
|                     | **FastFlow**         | 60.00%   |
|                     | **PatchCore**        | 80.00%   |
|                     | **Reverse Distillation** | 71.43% |
|                     | **STFPM**            | 85.71%  |
| **Dying 2**         | **CFlow**            | 14.29%   |
|                     | **FastFlow**         | 57.14%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Dying 3**         | **CFlow**            | 33.33%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Hue Down 15**     | **CFlow**            | 20.00%   |
|                     | **FastFlow**         | 0.40%    |
|                     | **PatchCore**        | 0.40%    |
|                     | **Reverse Distillation** | 0.40%  |
|                     | **STFPM**            | 0.40%   |
| **Hue Down 30**     | **CFlow**            | 25.00%   |
|                     | **FastFlow**         | 37.50%   |
|                     | **PatchCore**        | 25.00%   |
|                     | **Reverse Distillation** | 0.75%  |
|                     | **STFPM**            | 0.75%   |

##### Week 18
| Variable            | Model                | Accuracy |
|---------------------|----------------------|----------|
| **Normal**          | **CFlow**            | 56.25%   |
|                     | **FastFlow**         | 100.00%  |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.7** | **CFlow**          | 38.89%   |
|                     | **FastFlow**         | 88.89%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 94.44% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Down 0.9** | **CFlow**          | 33.33%   |
|                     | **FastFlow**         | 86.67%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 86.67% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.1** | **CFlow**            | 47.37%   |
|                     | **FastFlow**         | 89.47%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Contrast Up 1.3** | **CFlow**            | 40.00%   |
|                     | **FastFlow**         | 85.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 90.00% |
|                     | **STFPM**            | 100.00%  |
| **Dying 1**         | **CFlow**            | 42.86%   |
|                     | **FastFlow**         | 47.62%   |
|                     | **PatchCore**        | 95.24%   |
|                     | **Reverse Distillation** | 80.95% |
|                     | **STFPM**            | 85.71%  |
| **Dying 2**         | **CFlow**            | 45.45%   |
|                     | **FastFlow**         | 81.82%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 90.91%  |
| **Dying 3**         | **CFlow**            | 55.00%   |
|                     | **FastFlow**         | 95.00%   |
|                     | **PatchCore**        | 100.00%  |
|                     | **Reverse Distillation** | 100.00% |
|                     | **STFPM**            | 100.00%  |
| **Hue Down 15**     | **CFlow**            | 12.50%   |
|                     | **FastFlow**         | 18.75%   |
|                     | **PatchCore**        | 18.75%   |
|                     | **Reverse Distillation** | 25.00% |
|                     | **STFPM**            | 0.31%   |
| **Hue Down 30**     | **CFlow**            | 35.00%   |
|                     | **FastFlow**         | 0.95%    |
|                     | **PatchCore**        | 0.95%    |
|                     | **Reverse Distillation** | 60.00% |
|                     | **STFPM**            | 90.00%  |

## Detailed Results
### Metrics Table
| Week   | Model                | Accuracy | Precision | Recall | F1 Score | Specificity | False Positive Rate | False Negative Rate | Balanced Accuracy | Youden's Index (J) | Negative Predictive Value | AUROC  | AUPR   |
|--------|----------------------|----------|-----------|--------|----------|-------------|----------------------|----------------------|-------------------|--------------------|--------------------------|--------|--------|
| Week 3 | **CFlow**            | 57.50%   | 63.64%    | 35.00% | 45.16%   | 80.00%      | 20.00%               | 65.00%               | 57.50%            | 15.00%             | 55.17%                  | 81.00% | 82.69% |
|        | **FastFlow**         | 72.50%   | 100.00%   | 45.00% | 62.07%   | 100.00%     | 0.00%                | 55.00%               | 72.50%            | 45.00%             | 64.52%                  | 68.50% | 72.28% |
|        | **PatchCore**        | 72.50%   | 100.00%   | 45.00% | 62.07%   | 100.00%     | 0.00%                | 55.00%               | 72.50%            | 45.00%             | 64.52%                  | 79.25% | 83.09% |
|        | **Reverse Distillation** | 63.41% | 75.00% | 42.86% | 54.55%   | 85.00%      | 15.00%               | 57.14%               | 63.93%            | 27.86%             | 58.62%                  | 76.75% | 76.45% |
|        | **STFPM**            | 75.61%   | 92.31%    | 57.14% | 70.59%   | 95.00%      | 5.00%                | 42.86%               | 76.07%            | 52.14%             | 67.86%                  | 75.75% | 81.79% |
| Week 8 | **CFlow**            | 57.55%   | 72.22%    | 24.53% | 36.62%   | 90.57%      | 9.43%                | 75.47%               | 57.55%            | 15.09%             | 54.55%                  | 75.99% | 84.75% |
|        | **FastFlow**         | 76.42%   | 91.18%    | 58.49% | 71.26%   | 94.34%      | 5.66%                | 41.51%               | 76.42%            | 52.83%             | 69.44%                  | 76.68% | 75.99% |
|        | **PatchCore**        | 81.13%   | 100.00%   | 62.26% | 76.74%   | 100.00%     | 0.00%                | 37.74%               | 81.13%            | 62.26%             | 72.60%                  | 84.12% | 89.04% |
|        | **Reverse Distillation** | 81.13% | 97.14% | 64.15% | 77.27%   | 98.11%      | 1.89%                | 35.85%               | 81.13%            | 62.26%             | 73.24%                  | 85.62% | 88.83% |
|        | **STFPM**            | 87.85%   | 100.00%   | 75.47% | 86.02%   | 100.00%     | 0.00%                | 24.53%               | 87.74%            | 75.47%             | 80.60%                  | 80.69% | 77.17% |
| Week 12| **CFlow**            | 48.21%   | 46.15%    | 21.43% | 29.27%   | 75.00%      | 25.00%               | 78.57%               | 48.21%            | -3.57%             | 48.84%                  | 7.14%  | 75.00% |
|        | **FastFlow**         | 66.07%   | 71.43%    | 53.57% | 61.22%   | 78.57%      | 21.43%               | 46.43%               | 66.07%            | 32.14%             | 62.86%                  | 78.83% | 78.49% |
|        | **PatchCore**        | 82.14%   | 100.00%   | 64.29% | 78.26%   | 100.00%     | 0.00%                | 35.71%               | 82.14%            | 64.29%             | 73.68%                  | 75.77% | 70.91% |
|        | **Reverse Distillation** | 82.14% | 84.62% | 78.57% | 81.48%   | 85.71%      | 14.29%               | 21.43%               | 82.14%            | 64.29%             | 80.00%                  | 73.09% | 71.60% |
|        | **STFPM**            | 91.07%   | 100.00%   | 82.14% | 90.20%   | 100.00%     | 0.00%                | 17.86%               | 91.07%            | 82.14%             | 84.85%                  | 76.59% | 66.63% |
| Week 18| **CFlow**            | 40.91%   | 40.48%    | 38.64% | 39.53%   | 43.18%      | 56.82%               | 61.36%               | 40.91%            | -18.18%            | 41.30%                  | 17.88% | 34.60% |
|        | **FastFlow**         | 78.98%   | 86.96%    | 68.18% | 76.43%   | 89.77%      | 10.23%               | 31.82%               | 78.98%            | 57.95%             | 73.83%                  | 91.43% | 93.03% |
|        | **PatchCore**        | 91.48%   | 100.00%   | 82.95% | 90.68%   | 100.00%     | 0.00%                | 17.05%               | 91.48%            | 82.95%             | 85.44%                  | 91.86% | 94.11% |
|        | **Reverse Distillation** | 83.52% | 92.75% | 72.73% | 81.53%   | 94.32%      | 5.68%                | 27.27%               | 83.52%            | 67.05%             | 77.57%                  | 88.78% | 90.46% |
|        | **STFPM**            | 90.34%   | 100.00%   | 80.68% | 89.31%   | 100.00%     | 0.00%                | 19.32%               | 90.34%            | 80.68%             | 83.81%                  | 97.48% | 97.95% |

[Refer to the generated plots and metrics for detailed insights.](./result.xlsx)

"""
==============================================================================
Cost-Sensitive Sandstorm Hazard Classifier
Asymmetric Cost Matrix & Focal Re-weighting for Severe Meteorological Hazards
==============================================================================
"""

import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import confusion_matrix, classification_report


class CostSensitiveHazardClassifier:
    """
    Cost-Sensitive Sandstorm Severity Classifier.
    Addresses severe class imbalance (<1.5% extreme events) by imposing
    asymmetric cost weights penalizing False Negatives heavily.
    """

    def __init__(self, n_classes: int = 5, max_iter: int = 150, seed: int = 42):
        self.n_classes = n_classes
        self.max_iter = max_iter
        self.seed = seed
        self.model = None
        # Asymmetric class penalty weights: Severe Sandstorm (Class 4) has 20x weight
        self.class_weights = {0: 1.0, 1: 2.5, 2: 5.0, 3: 10.0, 4: 20.0}

    def fit(self, X_train: np.ndarray, y_hazard_train: np.ndarray):
        """Fit cost-sensitive classifier with sample weighting."""
        sample_weights = np.array([self.class_weights.get(int(y), 1.0) for y in y_hazard_train], dtype=np.float32)

        self.model = HistGradientBoostingClassifier(
            max_iter=self.max_iter,
            random_state=self.seed
        )
        self.model.fit(X_train, y_hazard_train, sample_weight=sample_weights)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)

    def evaluate(self, X_test: np.ndarray, y_true: np.ndarray) -> Dict[str, Any]:
        """
        Compute meteorological operational verification metrics:
        Threat Score (TS = Hits / (Hits + FalseAlarms + Misses))
        Probability of Detection (POD = Hits / (Hits + Misses))
        False Alarm Rate (FAR = FalseAlarms / (Hits + FalseAlarms))
        """
        y_pred = self.predict(X_test)
        cm = confusion_matrix(y_true, y_pred, labels=list(range(self.n_classes)))

        # Binary contingency analysis for dust occurrence (Hazard >= 1)
        true_dust = (y_true >= 1)
        pred_dust = (y_pred >= 1)

        hits = int(np.sum(true_dust & pred_dust))
        misses = int(np.sum(true_dust & ~pred_dust))
        false_alarms = int(np.sum(~true_dust & pred_dust))
        correct_negatives = int(np.sum(~true_dust & ~pred_dust))

        denominator_ts = hits + misses + false_alarms
        threat_score = float(hits / denominator_ts) if denominator_ts > 0 else 0.0

        denominator_pod = hits + misses
        pod = float(hits / denominator_pod) if denominator_pod > 0 else 0.0

        denominator_far = hits + false_alarms
        far = float(false_alarms / denominator_far) if denominator_far > 0 else 0.0

        # Multi-class accuracy
        accuracy = float(np.mean(y_true == y_pred))

        return {
            "overall_accuracy": accuracy,
            "threat_score_ts": round(threat_score, 4),
            "probability_of_detection_pod": round(pod, 4),
            "false_alarm_rate_far": round(far, 4),
            "contingency_counts": {
                "hits": hits,
                "misses": misses,
                "false_alarms": false_alarms,
                "correct_negatives": correct_negatives
            },
            "confusion_matrix": cm.tolist()
        }

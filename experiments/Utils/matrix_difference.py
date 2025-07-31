import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from transformers import AutoModelForCausalLM


class ModelDiffInspector:
    def __init__(self, base_model_path: str, finetuned_model_path: str):
        print("Loading models...")
        self.model_base = AutoModelForCausalLM.from_pretrained(base_model_path)
        self.model_finetuned = AutoModelForCausalLM.from_pretrained(finetuned_model_path)
        self.base_params = dict(self.model_base.named_parameters())
        self.finetuned_params = dict(self.model_finetuned.named_parameters())
        print("Models loaded.")

    def compute_l2_diffs(self):
        print("Computing L2 norm differences...")
        self.l2_diffs = {}
        for name in self.base_params:
            if name in self.finetuned_params:
                diff = torch.norm(self.base_params[name] - self.finetuned_params[name]).item()
                self.l2_diffs[name] = diff
        return self.l2_diffs

    def compute_cosine_diffs(self):
        print("Computing cosine similarity differences...")
        self.cosine_diffs = {}
        for name in self.base_params:
            if name in self.finetuned_params:
                flat_base = self.base_params[name].flatten()
                flat_finetuned = self.finetuned_params[name].flatten()
                cos_sim = F.cosine_similarity(flat_base, flat_finetuned, dim=0).item()
                self.cosine_diffs[name] = 1 - cos_sim  # 0 = identical, closer to 1 = more different
        return self.cosine_diffs

    def plot_top_changed_layers(self, metric: str = 'l2', top_n: int = 20):
        if metric == 'l2':
            if not hasattr(self, 'l2_diffs'):
                self.compute_l2_diffs()
            diffs = self.l2_diffs
            title = "Top Changed Layers (L2 Norm)"
        elif metric == 'cosine':
            if not hasattr(self, 'cosine_diffs'):
                self.compute_cosine_diffs()
            diffs = self.cosine_diffs
            title = "Top Changed Layers (Cosine Difference)"
        else:
            raise ValueError("Metric must be 'l2' or 'cosine'.")

        sorted_diffs = sorted(diffs.items(), key=lambda x: x[1], reverse=True)[:top_n]
        names = [name for name, _ in sorted_diffs]
        values = [val for _, val in sorted_diffs]

        plt.figure(figsize=(12, 6))
        plt.barh(names[::-1], values[::-1])
        plt.title(title)
        plt.xlabel("Difference")
        plt.tight_layout()
        plt.show()

    def find_added_removed_layers(self):
        print("Checking for added/removed layers...")
        base_keys = set(self.base_params.keys())
        fine_keys = set(self.finetuned_params.keys())

        added = fine_keys - base_keys
        removed = base_keys - fine_keys

        print(f"Added layers ({len(added)}): {added}")
        print(f"Removed layers ({len(removed)}): {removed}")
        return added, removed

    def summary(self, top_n=10):
        print("Summary Report:")
        l2 = self.compute_l2_diffs()
        cosine = self.compute_cosine_diffs()
        top_l2 = sorted(l2.items(), key=lambda x: x[1], reverse=True)[:top_n]
        top_cos = sorted(cosine.items(), key=lambda x: x[1], reverse=True)[:top_n]

        print("\nTop Changed Layers (L2 Norm):")
        for name, val in top_l2:
            print(f"  {name}: {val:.6f}")

        print("\nTop Changed Layers (Cosine Difference):")
        for name, val in top_cos:
            print(f"  {name}: {val:.6f}")

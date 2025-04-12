from aifd_cv_comparison.config.models import MODEL_REGISTRY
from aifd_cv_comparison.utils.model import Model

_loaded_models = {}
_is_loaded = False

def load_models():

    global _is_loaded

    if _is_loaded:
        print("[MODEL LOADER] Models already loaded. Skipping.")
        return

    print("[MODEL LOADER] Loading models...")

    for key, model in MODEL_REGISTRY.items():
        print(f" - Loading '{key}': {model['name']}")

        model = model

        _loaded_models[key] = model

    _is_loaded = True

    print("[MODEL LOADER] All models loaded.")


def get_model(name: str) -> Model:
    if not _is_loaded:
        raise RuntimeError("Models not loaded. Call `load_models()` first.")
    if name not in _loaded_models:
        raise KeyError(f"Model '{name}' not found. Available: {list(_loaded_models.keys())}")

    return Model(_loaded_models[name]['name'], _loaded_models[name]['model'], _loaded_models[name]['tokenizer'])

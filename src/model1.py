from transformers import AutoConfig, AutoModelForTokenClassification
from labels import LABEL2ID, ID2LABEL


def create_model(
    model_name: str,
    hidden_dropout_prob: float = 0.2,
    attention_dropout_prob: float = 0.2,
):
    config = AutoConfig.from_pretrained(
        model_name,
        num_labels=len(LABEL2ID),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
        hidden_dropout_prob=hidden_dropout_prob,
        attention_probs_dropout_prob=attention_dropout_prob,
    )
    model = AutoModelForTokenClassification.from_pretrained(model_name, config=config)
    return model

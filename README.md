# Loan Default Risk Assessment — Django + Machine Learning

**Python · Django · scikit-learn · XGBoost · SQLite · Celery/Redis (prototype)**

An academic loan-risk prototype with separate individual and business borrower flows. It stores borrower records in Django models and includes serialized logistic-regression and XGBoost estimators intended to estimate default probability. A small threshold-based decision function converts a probability into an *Approve* or *Deny* recommendation under different lender goals.

> **Portfolio scope:** This is an **educational prototype, not a credit-decision service**. The repository contains saved model artifacts but does not include the original training datasets, a reproducible model-training notebook or validated test-set performance reports. The prediction preprocessing is not fully verified against the saved models' expected feature schemas. Do **not** use this for real lending decisions or represent its outputs as fair, calibrated, or legally compliant.

## Architecture

~~~mermaid
flowchart LR
    A[Individual / business input forms] --> B[Django views]
    B --> C[Borrower-specific feature preprocessing]
    C --> D[Joblib XGBoost / logistic artifacts]
    D --> E[Estimated default probability]
    E --> F[Lender-goal threshold rule]
    F --> G[Prototype decision JSON]
    B --> H[(SQLite borrower records)]
~~~

## Repository structure

| Component | Location |
| --- | --- |
| Django app configuration | [lending_platform/](lending_platform/) |
| Borrower database models | [risk_assessment/models.py](risk_assessment/models.py) |
| Risk prediction endpoints | [risk_assessment/views.py](risk_assessment/views.py) |
| Feature construction and model loading | [risk_assessment/utils.py](risk_assessment/utils.py) |
| Deterministic decision rules | [risk_assessment/decision.py](risk_assessment/decision.py) |
| Saved model artifacts | [ml_models/](ml_models/) |
| UI templates | [risk_assessment/templates/](risk_assessment/templates/) |
| Unit tests | [risk_assessment/tests.py](risk_assessment/tests.py) |

## Run locally

Requires a supported Python 3 environment and the dependencies in \`requirements.txt\`. The serialized models were produced using older dependency versions and **may require compatible Python/scikit-learn/XGBoost versions** for loading. Joblib/pickle files must only be loaded from trusted sources.

~~~bash
git clone https://github.com/Akshat3004/Machine-Learning-Final-Project.git
cd Machine-Learning-Final-Project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DJANGO_DEBUG=true
python manage.py migrate
python manage.py runserver
~~~

Visit \`http://127.0.0.1:8000/risk_assessment/\` for the landing page. Routes defined in the repository include:

| Route | Function |
| --- | --- |
| \`/risk_assessment/\` | Prototype home page |
| \`/risk_assessment/individual/form/\` | Individual borrower form |
| \`/risk_assessment/business/form/\` | Business borrower form |
| \`/risk_assessment/individual/predict/\` | Individual probability JSON endpoint (POST) |
| \`/risk_assessment/business/predict/\` | Business probability JSON endpoint (POST) |
| \`/risk_assessment/individuals/\` | Borrower list |
| \`/risk_assessment/businesses/\` | Borrower list |

**Important:** The prediction handlers are *not* validated for arbitrary input; no working end-to-end prediction or model-quality metric is claimed. The form templates and Django ModelForms are not the same mechanism, and some original model preprocessing assumes features that may be unavailable at application time.

## Tests

~~~bash
python manage.py test risk_assessment
~~~

The included unit tests exercise the **decision rule** and **form schemas**. They do not evaluate loan model quality, real-world fairness, feature pipeline consistency, or live serving correctness.

## Security and limitations

- The original repository committed a Django development secret key. The settings now read \`DJANGO_SECRET_KEY\` from the environment, require it when \`DJANGO_DEBUG=false\`, and use only a clearly marked development fallback locally. **Rotate any secret that was reused outside local development**, because removing it from current files does not erase Git history.
- The original repository also tracked an entire \`venv/\` directory. Keep virtual environments untracked; recreate one using the commands above.
- The application currently uses SQLite for development. Celery tasks are prototypes and refer to some borrower fields that do not match the current Django models; they have **not been validated**.
- Serialized ML artifacts may carry unsafe pickle content if supplied by an untrusted party. Never load arbitrary model files.
- The business feature builder references outcomes such as charge-off principal, which would be **post-outcome leakage** if used to decide a new applicant's risk. This needs review and retraining before any real application.
- The project has no verified accuracy, ROC AUC, fairness, or calibration benchmark in this repository; none are claimed.
- Do not expose unauthenticated borrower lists or financial records on the public internet.

## Next improvements

1. Rebuild and version the data preprocessing pipeline and expected feature list alongside each model.
2. Re-train models using **only features available at decision time**; perform a temporal or borrower-disjoint validation split and assess calibration/fairness.
3. Replace prototype views with validated request schemas, error handling and authentication.
4. Fix or remove the outdated Celery tasks and add end-to-end integration tests.
5. Produce reproducible evaluation reports, screenshots and deployment configuration only after verifying the application.

The project showcases Django integration with model artifacts and a policy-based decision layer, not a production underwriting system.

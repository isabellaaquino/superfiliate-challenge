# Demonstration screenshot

![image](https://github.com/user-attachments/assets/395e4449-831a-4310-87d8-3ecc077c8b40)

---

## Prerequisites

- Python 3.12 or higher
- `pip` (Python package installer)

## Steps

1. **Clone Your Repository**

   ```bash
   git clone https://github.com/isabellaaquino/superfiliate-challenge.git
   cd superfiliate-challenge
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Project Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**

   To run your FastAPI application locally:

   ```bash
   uvicorn main:app --reload
   ```

   Access it at `http://127.0.0.1:8000`.

:exclamation: **PS**: You can trigger a local pipeline run by running `tox`, and run the tests locally by running `pytest`.

### Configuration

To setup the discount configuration, you can do that by navigating to the file `config.json`. There you can list all the excluded collections and the discount progression as you wish.

Example of the default configuration:

```json
{
  "discount_rule": {
    "min_qty": 2,
    "discount_percentage": 5.0
  },
  "excluded_collections": ["KETO"]
}
```

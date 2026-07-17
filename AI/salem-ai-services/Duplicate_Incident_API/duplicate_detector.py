from sklearn.metrics.pairwise import cosine_similarity


class DuplicateDetector:

    def __init__(self, model, embeddings, reports):

        self.model = model
        self.embeddings = embeddings
        self.reports = reports

    def check_duplicate(self, report_text):

        report_embedding = self.model.encode(
            [report_text]
        )

        similarities = cosine_similarity(
            report_embedding,
            self.embeddings
        )[0]

        best_idx = similarities.argmax()

        best_score = similarities[best_idx]

        # لو أقل من Threshold
        if best_score < 0.85:

            return {
                "duplicate": False,
                "similarity": round(float(best_score), 4),
                "matched_report": None,
                "threshold": 0.85
            }

        # لو Duplicate
        return {
            "duplicate": True,
            "similarity": round(float(best_score), 4),
            "matched_report":
                self.reports.iloc[best_idx]["description"],
            "threshold": 0.85
        }
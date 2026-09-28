class GeminiDocumentGenerator:

    def generate_document(self, document_type, language, details):
        return (
            f"Document Type: {document_type}\n"
            f"Language: {language}\n\n"
            f"Draft:\n{details}\n\n"
            "Note: This is a sample draft. "
            "Please consult a qualified legal professional."
        )
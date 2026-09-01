from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.file_utils import read_file
from api.agents.extractor_agent import process_medical_note
from api.agents.generator_agent import generate_initial_response
from api.agents.solver_agent import answer_question, review_initial_response
from api.agents.refiner_agent import refine_response
from api.utils.cache_utils import get_cached_data

class UploadNoteView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "File is required."}, status=400)
        try:
            file_content = read_file(file)
            extracted_terms, verified_definitions = process_medical_note(file_content)

            return Response({
                "extracted_terms": extracted_terms,
                "verified": verified_definitions
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get("question", "").strip()
        medical_note = get_cached_data("medical_note_content")
        verified_definitions = get_cached_data("verified_definitions")

        if not question:
            return Response({"error": "Question is required."}, status=400)
        if not medical_note:
            return Response({"error": "Medical note is required. Please upload a medical note first."}, status=400)
        if not verified_definitions:
            return Response({"error": "Verified definitions are required. Please process the medical note first."}, status=400)

        try:
            initial_response = generate_initial_response(question, medical_note)

            feedback = review_initial_response(initial_response, medical_note, verified_definitions)

            refined_response = refine_response(question, feedback, initial_response, medical_note)

            return Response({
                "question": question,
                "initial_response": initial_response,
                "feedback": feedback,
                "refined_response": refined_response
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
import os
import random
import string
import uuid

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.tokens import BearerTokenAuthentication
from files.models import File


class FileUploadView(APIView):
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
    ALLOWED_EXTENSIONS = {'doc', 'pdf', 'docx', 'zip', 'jpeg', 'jpg', 'png'}

    model = File
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]

    def generate_file_id(self):
        while True:
            file_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            if not self.model.objects.filter(file_id=file_id).exists():
                break

        return file_id

    def correct_filename(self, user, filename):
        base, ext = os.path.splitext(filename)

        existing_filenames = set(File.objects.filter(owner=user).values_list('name', flat=True))

        new_filename = filename
        i = 0
        while new_filename in existing_filenames:
            i += 1
            new_filename = f'{base} ({i}){ext}'
        return new_filename

    def check_extension(self, filename):
        base, ext = os.path.splitext(filename)
        return ext[1:] in self.ALLOWED_EXTENSIONS

    def post(self, request):
        files = request.FILES.getlist('files')

        response_infos = []

        for i, file in enumerate(files):
            if file.size > self.MAX_FILE_SIZE:
                response_infos.append({"success": False,
                                       "message": {"size": "size of file is too large"},
                                       "name": file.name})
            if not self.check_extension(file.name):
                if len(response_infos) == i:
                    response_infos.append({"success": False,
                                           "message": {"extension": "file extension is incorrect"},
                                           "name": file.name})
                else:
                    response_infos[-1]["message"]["extension"] = "file extension is incorrect"

            if len(response_infos) != i:
                continue

            file_model = File(name=self.correct_filename(request.user, file.name),
                              file_id = self.generate_file_id(),
                              owner=request.user)

            if not os.path.exists(settings.MEDIA_ROOT / request.user.email):
                os.mkdir(settings.MEDIA_ROOT / request.user.email)

            with open(settings.MEDIA_ROOT / request.user.email / file_model.name, 'wb') as f:
                f.write(file.read())

            file_model.save()

            response_infos.append({"success": True,
                                   "message": "Success",
                                   "name": file_model.name,
                                   "url": f'{request.META.get("HTTP_HOST")}/files/{file_model.file_id}',
                                   "file_id": file_model.file_id})
        return Response(response_infos, status=status.HTTP_200_OK)


class FileRetrieveView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]
    model = File

    def check_file_permissions(self, request, file):
        if not file.check_permissions(request.user):
            self.permission_denied(request,
                                   f"You do not have permission to {file.file_id}",
                                   status.HTTP_403_FORBIDDEN)


    def get(self, request, file_id):
        file = get_object_or_404(self.model, file_id=file_id)

        self.check_file_permissions(request, file)

        file_path = settings.MEDIA_ROOT / request.user.email / file.name

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        return response

from rest_framework.permissions import BasePermission


class IsDoctorOwnerOrReadOnly(BasePermission):
    """
    Allow authenticated users to read doctors.
    Only the creator can update or delete a doctor.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return obj.created_by == request.user
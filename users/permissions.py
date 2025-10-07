from rest_framework.permissions import BasePermission
    
class IsOrganizationMember(BasePermission):
    """User must be member of the organization"""
    
class IsDepartmentMember(BasePermission):
    """User must be in the same department"""
    
class CanCreateUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ["admin", "supervisor"]:
            return True
        return False

class CanManageUsers(BasePermission):
    """User can manage other users (Admin/Supervisor only)"""
    
class CanManageDepartments(BasePermission):
    """User can manage departments (Admin only)"""
    
class CanAssignAgents(BasePermission):
    """User can assign agents to departments (Supervisor/Admin)"""
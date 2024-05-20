from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow admins or the owner of the object to update it.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # # # Read permissions are allowed to any request
        # if request.method in ['GET', 'HEAD', 'OPTIONS']:
        #     return True

        # Write permissions are only allowed to the owner or admins
        return request.user.role == 'admin' or obj == request.user
    


class OnlyAdmin(permissions.BasePermission):
        
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the role 'admin'
        return request.user.is_authenticated and request.user.role == 'admin'
    


class IsAdminOrCoach(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'coach')

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has the role 'admin'
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'coach')
    


class IsAdminOrCoachNoPlayer(permissions.BasePermission):

    def has_permission(self, request, view):      
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'coach')

    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated and has the role 'admin'
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'coach')
    


class IsAdminOrCoachOwner(permissions.BasePermission):    

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and (request.user.role == 'admin') #or request.user.role == 'coach' )
    
        
    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        # Check if the user is authenticated and has the role 'admin'
        return request.user.is_authenticated and (request.user.role == 'admin' or (request.user.role == 'coach' and obj.coach.id == request.user.id))
    


#Player Permissions
class IsAdminOrCoachPlayerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and (request.user.role == 'admin') or (request.user.role == 'coach')
    

    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        

        # Check if the user is authenticated and has the role 'admin'
        # if obj.team:
        #     return request.user.is_authenticated and (request.user.role == 'admin' or (request.user.role == 'coach' and obj.team.coach.id == request.user.id))
        return request.user.is_authenticated and (request.user.role == 'admin' or (request.user.role == 'coach'))




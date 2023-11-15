from service_objects.services import ServiceWithResult


class UserAuthService(ServiceWithResult):

    def process(self):
        return self

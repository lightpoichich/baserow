from baserow.core.exceptions import (
    InstanceTypeAlreadyRegistered,
    InstanceTypeDoesNotExist,
)


class TriggerTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class TriggerTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass

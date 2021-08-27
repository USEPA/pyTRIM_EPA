# These imports are necessary for running alembic
# with the --autogenerate flag:

# 1. Import the base Model class
from .utils.base import Model  # noqa

# 2. Import all model files
from .users.models import *  # noqa
from .scenarios.models import *  # noqa
from .environment.models import *  # noqa


from database.models.activity import ActivityModel
from database.models.organization import OrganizationModel
from database.models.organization_activities import OrganizationActivityModel


class OrganizationActivityManager:

    def __init__(self):
        pass

    @staticmethod
    def add_activity_to_organization(session, organization: "OrganizationModel", activity: "ActivityModel"):
        assoc = OrganizationActivityModel(organization=organization, activity=activity)
        session.add(assoc)
        session.commit()

organization_activity_manager = OrganizationActivityManager()

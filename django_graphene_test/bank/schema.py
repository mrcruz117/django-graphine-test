import graphene
import graphene_django
from .models import User


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    total_users = graphene.Int()

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_total_users(self, info):
        return User.objects.count()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        age = graphene.Int(required=True)
        balance = graphene.Decimal(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, name, email, age, balance):
        user = User(name=name, email=email, age=age, balance=balance)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        email = graphene.String()
        age = graphene.Int()
        balance = graphene.Decimal()

    def mutate(self, info, id, name, email, age, balance):
        user = User.objects.get(id=id)
        user.name = name
        user.email = email
        user.age = age
        user.balance = balance
        user.save()
        return UpdateUser(ok=True, user=user)


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = User.objects.get(id=id)
        user.delete()
        return DeleteUser(ok=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

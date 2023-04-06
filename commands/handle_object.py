from commands.check_collision import CheckCollision
from commands.macro_mass_collisions import MassCollisions
from interfaces.command import Command
from interfaces.uobject import UObject
from ioc.container import IoC
from mtypes.shape import Circle, Rect


class HandleObject(Command):
    def __init__(self, obj: UObject):
        self._obj = obj

    def execute(self):
        battle_field = IoC.resolve('BattleField', -1)
        queue = IoC.resolve('Queue', -1)

        regions = battle_field.get_property("regions")
        position = self._obj.get_property("position")
        radius = self._obj.get_property("radius")

        obj_regions = [
            region
            for region, obj_list in regions.items()
            if self.intersects(Circle(position.x, position.y, radius), region)
        ]

        for region, obj_list in regions.items():
            if region in obj_regions:
                if self._obj in obj_list:
                    continue
                else:
                    obj_list.append(self._obj)
                    queue.put(
                        MassCollisions(
                            [CheckCollision(self._obj, obj) for obj in obj_list]
                        )
                    )
            else:
                if self._obj in obj_list:
                    obj_list.remove(self._obj)
                else:
                    continue

    @staticmethod
    def intersects(circle: Circle, rect: Rect):

        circle_distance_x = abs(circle.x - (rect.x + rect.width / 2))
        circle_distance_y = abs(circle.y - (rect.y + rect.height / 2))

        if circle_distance_x > (rect.width / 2 + circle.r):
            return False
        if circle_distance_y > (rect.height / 2 + circle.r):
            return False

        if circle_distance_x <= (rect.width / 2):
            return True
        if circle_distance_y <= (rect.height / 2):
            return True

        corner_distance_sq = (circle_distance_x - rect.width / 2)**2 + \
            (circle_distance_y - rect.height / 2)**2

        return corner_distance_sq <= (circle.r**2)

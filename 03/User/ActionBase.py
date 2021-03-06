from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import GameControlProxy
from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition

from User.AttackFilter import DummyAttackFilter, EmptyAttackFilter


class ActionBase(IActionBase):
    """
    You can define here your custom actions. Methods must be public (not starting with __ or _) and must have unique
    names. Methods could have as many arguments as you want. Instance of this class will be available in
    Inference class.

    **This class provides:**

    * self.game_control_proxy [GameControlProxy] for doing actions in game
    * self.player [PlayerTag] instance of your player for identification yourself in proxy

    Usage of ActionBase is described in documentation.


    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!               TODO: Write implementation of your actions HERE                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    game_control_proxy: GameControlProxy
    player: PlayerTag

    def build_base_random(self, free_tile):
        # Custom log messages
        Logger.log('Building base')

        # Create instance of custom filter
        empty_filter = FilterFactory().attack_filter(EmptyAttackFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter, 'Base attacking')

        # Create instance of default filter
        strongest_filter = FilterFactory().attack_filter(AttackStrongestFilter)

        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             free_tile,
                             [empty_filter, dummy_filter, strongest_filter], []))

    def build_base(self, x, y):
        # Custom log messages
        Logger.log('Building base')

        # Create instance of custom filter
        empty_filter = FilterFactory().attack_filter(EmptyAttackFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter, 'Base attacking')

        # Create instance of default filter
        strongest_filter = FilterFactory().attack_filter(AttackStrongestFilter)

        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             OffsetPosition(x, y),
                             [empty_filter, dummy_filter, strongest_filter], []))

    def build_archer(self, visible_free_tile):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ARCHER,
                             visible_free_tile,
                             [], []))

    def build_magican(self, visible_free_tile):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICIAN,
                             visible_free_tile,
                             [], []))

    def build_ent(self, x, y):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             OffsetPosition(x, y), [], []))

    def build_ent_pos(self, position):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.ENT,
                             position, [], []))

    def build_knight(self, x, y):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.KNIGHT,
                             OffsetPosition(x, y), [], []))


    def build_knight_posb(self, visible_free_tile_bot):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.KNIGHT,
                             visible_free_tile_bot,
                             [], []))

    def build_knight_post(self, visible_free_tile_top):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.KNIGHT,
                             visible_free_tile_top,
                             [], []))
    def build_knight_posl(self, visible_free_tile_left):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.KNIGHT,
                             visible_free_tile_left,
                             [], []))

    def build_knight_posr(self, visible_free_tile_right):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.KNIGHT,
                             visible_free_tile_right,
                             [], []))


    def build_mag_posb(self, visible_free_tile_bot):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICAN,
                             visible_free_tile_bot,
                             [], []))

    def build_mag_post(self, visible_free_tile_top):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICAN,
                             visible_free_tile_top,
                             [], []))
    def build_mag_posl(self, visible_free_tile_left):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICAN,
                             visible_free_tile_left,
                             [], []))

    def build_mag_posr(self, visible_free_tile_right):
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.MAGICAN,
                             visible_free_tile_right,
                             [], []))

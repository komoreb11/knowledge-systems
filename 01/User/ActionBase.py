from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import GameControlProxy, MapProxy
from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Structure.Enums import GameObjectType, TerrainType
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition
from User.AttackFilter import DummyAttackFilter, EmptyAttackFilter


class ActionBase(IActionBase):
    """
    You can define here your custom actions. Methods must be public (not starting with __ or _) and must have unique
    names. Methods could have as many arguments as you want. Instance of this class will be available in
    Interference class.


    **This class provides:**

    * self.game_control_proxy [GameControlProxy] for doing actions in game
    * self.map_proxy [MapProxy] for finding places on map
    * self.player [IPlayer] instance of your player for identification yourself in proxy

    MapProxy should be used there only for finding right place on the map. For example functions like:
    * spawn_knight_on_nearest_mountain(x,y)
    * spawn_unit_near_to_base(amount_of_units, unit_type)
    * spawn_unit_far_in_direction(direction)
    * etc...

    It is forbidden, to create whole login in those functions. Whole behaviour logic must be editable without,
    touching code in ActionBase (login must mainly depend on rules). So it's forbidden to use functions like:
    * prepare_defence()
    * spawn_ideal_amount_of_units_at_ideal_places()
    * defend_my_base()
    * etc...

    You can use () operator on ActionBase instance to call your function by `str` name or `Expression` class.
    Expression class will also pass arguments from self to your method. () operator using only args so be careful about
    order and number of arguments.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!               TODO: Write implementation of your actions HERE                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    game_control_proxy: GameControlProxy
    map_proxy: MapProxy
    player: IPlayer

    def build_base(self):
        # Custom log messages
        Logger.log('Building base')

        # Create instance of custom filter
        empty_filter = FilterFactory().attack_filter(EmptyAttackFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter, 'Base attacking')

        # Create instance of default filter
        strongest_filter = FilterFactory().attack_filter(AttackStrongestFilter)
        if self.map_proxy.get_terrain_type(OffsetPosition(0,
                                                          0)) != TerrainType.MOUNTAIN:  # check if 0 0 is a mountain(base will native have a damage every round)
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 GameObjectType.BASE,
                                 OffsetPosition(0, 0),
                                 [empty_filter, dummy_filter, strongest_filter], []))
        else:
            self.game_control_proxy.spawn_unit(
                SpawnInformation(self.player,
                                 GameObjectType.BASE,
                                 OffsetPosition(0, 1),
                                 [empty_filter, dummy_filter, strongest_filter], []))

    def set_knights_base(self):

        Logger.log('Setting knights above base')
        k = self.map_proxy.get_bases_positions()
        qbase = self.map_proxy.compute_visible_tiles(OffsetPosition(0, 0), 1)
        for i in k:
            qbase = self.map_proxy.compute_visible_tiles(i, 1)
        k = 0
        for i in qbase:
            if (not self.player.map_proxy.is_position_occupied(i)) and self.player.game_object_proxy.get_resources(
                    self.player) > 9:
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     GameObjectType.KNIGHT,
                                     i,
                                     [], []))
                k += 1

    def spawn_on_river(self):
        Logger.log('Riverside defence')
        vis = self.map_proxy.get_player_visible_tiles()
        qbase = self.map_proxy.compute_visible_tiles(OffsetPosition(0, 0), 1)
        for i in vis:
            if self.map_proxy.get_terrain_type(i) == TerrainType.RIVER:
                qbase = self.map_proxy.compute_visible_tiles(i, 1)
                for j in qbase:
                    if self.map_proxy.get_terrain_type(
                            j) != TerrainType.RIVER and self.player.game_object_proxy.get_resources(
                        self.player) > 9 and not self.player.map_proxy.is_position_occupied(
                        j) and j not in self.map_proxy.get_border_tiles() and j in self.map_proxy.get_player_visible_tiles():
                        self.game_control_proxy.spawn_unit(
                            SpawnInformation(self.player,
                                             GameObjectType.KNIGHT,
                                             j,
                                             [], []))

    def spawn_knights_in_villages(self):
        Logger.log('Setting village defence')
        vis = self.map_proxy.get_player_visible_tiles()
        for i in vis:
            if self.map_proxy.get_terrain_type(i) == TerrainType.VILLAGE and not self.map_proxy.is_position_occupied(
                    i) and self.player.game_object_proxy.get_resources(
                self.player) > 9:
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     GameObjectType.KNIGHT,
                                     i,
                                     [], []))

    def spawn_scout(self):
        Logger.log('Spawn scout')
        vis = self.map_proxy.get_player_visible_tiles()
        k = 0
        for i in vis:
            if self.map_proxy.get_terrain_type(i) == TerrainType.HILL and not self.map_proxy.is_position_occupied(
                    i) and (abs(i.q) + abs(
                i.r)) >= 3 and i not in self.map_proxy.get_border_tiles() and self.player.game_object_proxy.get_resources(
                self.player) > 4 and k < 1:
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     GameObjectType.ARCHER,
                                     i,
                                     [], []))
                k += 1
                if (k > 2):
                    break

    def spawn_deamon_killers(self):
        Logger.log('Daemon must die')
        vis = self.map_proxy.get_player_visible_tiles()
        qbase = self.map_proxy.compute_visible_tiles(OffsetPosition(0, 0), 1)
        kk = 0
        for i in vis:
            if self.game_object_proxy.get_object_type(i) == GameObjectType.DAEMON:
                qbase = self.map_proxy.compute_visible_tiles(i, 1)
                for j in qbase:
                    if self.map_proxy.is_position_occupied(
                            j) or j in self.map_proxy.get_border_tiles() or self.map_proxy.get_terrain_type(
                        i) == TerrainType.MOUNTAIN:
                        del j
                    else:
                        if kk == 0 and self.player.game_object_proxy.get_resources(
                                self.player) > 9:
                            self.game_control_proxy.spawn_unit(
                                SpawnInformation(self.player,
                                                 GameObjectType.KNIGHT,
                                                 j,
                                                 [], []))
                            kk += 1
                        elif kk == 1:
                            if self.player.game_object_proxy.get_resources(self.player) > 49:
                                self.game_control_proxy.spawn_unit(
                                    SpawnInformation(self.player,
                                                     GameObjectType.ENT,
                                                     j,
                                                     [], []))
                            elif self.player.game_object_proxy.get_resources(self.player) > 9:
                                self.game_control_proxy.spawn_unit(
                                    SpawnInformation(self.player,
                                                     GameObjectType.KNIGHT,
                                                     j,
                                                     [], []))

                            kk += 1

    """def spawn_ent_forest(self):
        vis = self.map_proxy.get_player_visible_tiles()
        qbase = self.map_proxy.compute_visible_tiles(OffsetPosition(0, 0), 1)
        kk = 0
        for i in vis:
            if (not self.map_proxy.is_position_occupied(i)) and self.map_proxy.get_terrain_type(
                        i) == TerrainType.FOREST and (i not in self.map_proxy.get_border_tiles()):
                self.game_control_proxy.spawn_unit(
                                SpawnInformation(self.player,
                                                 GameObjectType.ENT,
                                                 i,
                                                 [], []))"""

    def spawn_ent_forest(self):
        vis = self.map_proxy.get_player_visible_tiles()
        for i in vis:
            if (not self.map_proxy.is_position_occupied(i)) and self.map_proxy.get_terrain_type(
                    i) == TerrainType.FOREST and (
                    i not in self.map_proxy.get_border_tiles()) and self.player.game_object_proxy.get_resources(
                self.player) > 49:
                self.game_control_proxy.spawn_unit(
                    SpawnInformation(self.player,
                                     GameObjectType.ENT,
                                     i,
                                     [], []))

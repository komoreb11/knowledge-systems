from typing import List
from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType, EffectType, GameRole
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition, AxialPosition
import random

class KnowledgeBase(IKnowledgeBase):
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Inference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** - Proxy for access to map information
    - **game_object_proxy [GameObjectProxy]** - Proxy for access to all game object information
    - **uncertainty_proxy [UncertaintyProxy]** - Proxy for access to all uncertainty information in game
    - **player [PlayerTag]** - class that serve as instance of user player for identification in proxy methods

    """
    map_proxy: MapProxy
    game_object_proxy: GameObjectProxy
    game_uncertainty_proxy: GameUncertaintyProxy
    player: PlayerTag

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: PlayerTag):
        """
        You can add some code to __init__ function, but don't change the signature. You cannot initialize
        KnowledgeBase class manually so, it is make no sense to change signature.
        """
        super().__init__(map_proxy, game_object_proxy, game_uncertainty_proxy, player)

    def create_knowledge_base(self) -> List[Fact]:
        """
        Method for create user knowledge base. You can also have other class methods, but entry point must be this
        function. Don't change the signature of the method, you can change return value, but it is not recommended.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!  TODO: Write implementation of your knowledge base definition HERE   !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        facts = []

        # Add bool fact
        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))
        # Add fact with data holder
        # We can use there eval function same as data function
        # because if first_free_tile return None, bool value of None is False, otherwise bool value is True
        # You can use different functions for eval and data
        facts.append(Fact('free_tile', eval_function=self.first_free_tile, data=self.first_free_tile))
        facts.append(Fact('visible_free_tile', eval_function=self.visible_free_tile, data=self.visible_free_tile))
        facts.append(Fact('not_a_mountain', eval_function=self.not_a_mountain, data=self.not_a_mountain))
        facts.append(Fact('a_mountain', eval_function=self.a_mountain, data=self.a_mountain))
        facts.append(Fact('is_empty_position', eval_function=self.is_empty, data=self.is_empty))
        facts.append(Fact('is_base_position', eval_function=self.is_basepos, data=self.is_basepos))
        facts.append(Fact('riverside_tile', eval_function=self.riverside_tile, data=self.riverside_tile))
        # Add numerical fact
        facts.append(Fact("money", lambda: self.game_object_proxy.get_resources(self.player)))

        return facts

    def not_a_mountain(self, x, y):
        return self.map_proxy.get_terrain_type(OffsetPosition(x, y)) != TerrainType.MOUNTAIN

    def is_basepos(self, x, y):
        for i in self.map_proxy.get_bases_positions():
            if i == OffsetPosition(x, y):
                return 1
        return 0

    def a_mountain(self, x, y):
        return self.map_proxy.get_terrain_type(OffsetPosition(x, y)) == TerrainType.MOUNTAIN

    def is_empty(self, x, y):
        return not self.map_proxy.is_position_occupied(OffsetPosition(x, y))


    def first_free_tile(self, terrain_type: str):
        """ Find random tile with given terrain type """
        tiles = self.map_proxy.get_inner_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            if terrain and position not in border_tiles:
                return position
        return None

    def visible_free_tile(self, terrain_type: str):
        """ Find random free tile with given terrain type """
        tiles = self.map_proxy.get_player_visible_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            occupied = self.map_proxy.is_position_occupied(position)
            if terrain and not occupied and position not in border_tiles:
                return position
        return None

    def riverside_tile(self):
        vis = self.visible_free_tile('river')
        qbase = self.map_proxy.compute_visible_tiles(vis, 1)
        if qbase is None:
            return vis
        k = qbase.pop()
        for k in qbase:
            if(qbase and self.map_proxy.get_terrain_type(k) != TerrainType.RIVER and not self.map_proxy.is_position_occupied(k) and k is not None):
                return k
        return vis



def possible_spawn_tiles(self):
    """ Get list of possible tiles, where enemy spawn a unit """
    spawn_info = self.game_uncertainty_proxy.spawn_information()

    next_round = spawn_info[0]

    possible_tiles = set()
    for unit in next_round:
        possible_tiles.update([x.position for x in unit.positions])

    return possible_tiles

def daemon_form_top(self, kek):
    print(kek)
    return 1

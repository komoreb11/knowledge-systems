from typing import List, Set

from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Structure.Enums import GameObjectType, TerrainType
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototype


class KnowledgeBase(IKnowledgeBase):
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Interference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** - Proxy for access to map information
    - **game_object_proxy [GameObjectProxy]** - Proxy for access to all game object information
    - **uncertainty_proxy [UncertaintyProxy]** - Proxy for access to all uncertainty information in game
    - **player [IPlayer]** - instance of user player for identification in proxy methods

    """
    map_proxy: MapProxy
    game_object_proxy: GameObjectProxy
    game_uncertainty_proxy: GameUncertaintyProxy
    player: IPlayer
    terrain_type: TerrainType

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: IPlayer):
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

        # info about a base

        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))
        else:
            facts.append(Fact('player_have_base'))

        # map check
        vis = self.map_proxy.get_player_visible_tiles()
        for i in vis:
            if self.map_proxy.get_terrain_type(i) == TerrainType.RIVER:
                facts.append(Fact('there_is_river'))
                print('river')
            if self.map_proxy.get_terrain_type(i) == TerrainType.VILLAGE:
                facts.append(Fact('there_is_village'))
                print('village')
            if self.map_proxy.get_terrain_type(i) == TerrainType.FOREST:
                facts.append(Fact('there_is_forest'))
                print('hill')
                break

        # so we need to know how much scouts we already have, to place more if we need
        arc = 0
        for i in self.map_proxy.get_player_visible_tiles():
            if self.game_object_proxy.get_object_type(i) == GameObjectType.ARCHER:
                arc += 1
        if arc < 3: #2 scouts on map is an optimus
            facts.append(Fact('can_place_scouts'))

        # enemies
        """for i in self.map_proxy.get_player_visible_tiles():
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.demon:
                facts.append(Fact('daemom_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.cyclop:
                facts.append(Fact('cyclop_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.ELEMENTAL:
                facts.append(Fact('elemental_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.GARGOYLE:
                facts.append(Fact('gargoyle_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.MINOTAUR:
                facts.append(Fact('minotaur_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.NECROMANCER:
                facts.append(Fact('necromancer_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.ORC:
                facts.append(Fact('orc_is_here'))
            if self.game_object_proxy.get_object_type(i) == GameObjectPrototype.SKELETON:
                facts.append(Fact('skeleton_is_here'))"""

        # Add numerical fact
        user_resources = self.game_object_proxy.get_resources(self.player)
        facts.append(Fact("money", lambda: user_resources))

        return facts

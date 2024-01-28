import random
from src.game_constants import SnipePriority, TowerType
from src.robot_controller import RobotController
from src.player import Player
from src.map import Map

class BotPlayer(Player):
    def __init__(self, map: Map):
        self.map = map
        self.x = map.width
        self.y = map.height
        self.gscore = [[0]*self.x for _ in range(self.y)]
        self.bscore = [[0]*self.x for _ in range(self.y)]
        self.srscore = [[0]*self.x for _ in range(self.y)]
        for i in range(self.y):
            for j in range(self.x):
                if map.is_space(i, j):
                    for ii in range(self.x):
                        for jj in range(self.y):
                            if not map.is_path(ii, jj):
                                continue
                            if((ii-i)**2+(jj-j)**2<60):
                                self.gscore[i][j] += 10
                            if((ii-i)**2+(jj-j)**2<10):
                                self.bscore[i][j] += 60
                                

    def play_turn(self, rc: RobotController):
        self.build_towers(rc)
        self.towers_attack(rc)

    def build_towers(self, rc: RobotController):
        build = False
        balance = rc.get_balance(rc.get_ally_team())
        gs, gi, gj = 0,0,0
        bs, bi, bj = 0,0,0
        for i in range(self.x):
            for j in range(self.y):
                if self.gscore[i][j] > gs:
                    build = True
                    gs = self.gscore[i][j]
                    gi, gj = i, j
                if self.bscore[i][j] > bs:
                    build = True
                    bs = self.bscore[i][j]
                    bi, bj = i, j
        if(gs == 0 or bs == 0 or balance < 1750):
            return
        
        if(bs >= gs) and  rc.can_build_tower(TowerType.BOMBER, bi, bj):
            rc.build_tower(TowerType.BOMBER, bi, bj)
            self.gscore[bi][bj] = self.bscore[bi][bj] = 0
        elif rc.can_build_tower(TowerType.GUNSHIP, gi, gj):
            rc.build_tower(TowerType.GUNSHIP, gi, gj)
            self.gscore[gi][gj] = self.bscore[gi][gj] = 0
        
    
    def towers_attack(self, rc: RobotController):
        towers = rc.get_towers(rc.get_ally_team())
        for tower in towers:
            if tower.type == TowerType.GUNSHIP:
                rc.auto_snipe(tower.id, SnipePriority.STRONG)
            elif tower.type == TowerType.BOMBER:
                rc.auto_bomb(tower.id)

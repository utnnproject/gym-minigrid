#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gym_minigrid.minigrid import *
from gym_minigrid.register import register
import random


class FourRoomsEnv9x9(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=None, goal_pos=None):
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos
        super().__init__(grid_size=9, max_steps=1000)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 2
        room_h = height // 2

        # For each row of rooms
        for j in range(0, 2):

            # For each column
            for i in range(0, 2):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                # Bottom wall and door
                if i + 1 < 2:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, self._rand_int(yT + 1, yB))
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 2:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (self._rand_int(xL + 1, xR), yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        self.mission = 'Reach the goal'

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        return obs, reward, done, info



class NineRoomsLavaEnv16x16(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment with lava to avoid.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=(2,2), goal_pos=(13,13), obstacle_type=Lava, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=16, max_steps=10000)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        types = ['lava']
        
        objs = []
        idx = 0

        # For each object to be generated
        # while len(objs) < self.numObjs:
        #     objType = self._rand_elem(types)
        #     objColor = self._rand_elem(COLOR_NAMES)

        #     if objType == 'key':
        #         obj = Key(objColor)
        #     elif objType == 'ball':
        #         obj = Ball(objColor)
        #     elif objType == 'lava':
        #         obj = Lava()

        #     self.place_obj(obj,top=(0, idx))
        #     objs.append(obj)
        #     idx += 1
        
        # random the number of lavas
        noOfLavas = random.randint(3,6)

        for i in range(0, noOfLavas):
            obj = Lava()
            self.put_obj(obj, random.randint(2,12), random.randint(2,12))
            idx += 1
        
        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 3
        room_h = height // 3

        # For each row of rooms
        for j in range(0, 3):

            # For each column
            for i in range(0, 3):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                hor = self._rand_int(yT + 1, yB)

                ver = self._rand_int(xL + 1, xR)
                # Bottom wall and door
                if i + 1 < 3:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, hor)
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 3:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (ver, yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # Generate and store random gap position
        self.gap_pos = np.array((
            self._rand_int(2, width - 2),
            self._rand_int(1, height - 1),
        ))

        ## Place the obstacle wall
        #self.grid.vert_wall(self.gap_pos[0], 1, height - 2, self.obstacle_type)
        
        # Put a hole in the wall
        #self.grid.set(self.gap_pos, self.obstacle_type)
        
        #self.mission = 'Reach the goal'
        
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        # print(obs)
        # print(reward)
        # print(done)
        # print(info)
        # print ("=======")
        
        return obs, reward, done, info

class SimpleCorridor(MiniGridEnv):
    

    def __init__(self, agent_pos=None, goal_pos=None, obstacle_type=None, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=22, max_steps=100)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)
        

        self._agent_default_pos = (12 + self._rand_int(0, 8), 10 + self._rand_int(0, 2))

        # random goal type
        goalType = self._rand_int(1, 4)
        
        self.goal_type = goalType

        if (goalType == 1):
            goal_pos = (5,10 + self._rand_int(0, 2))
        elif (goalType == 2):
            goal_pos = (18 + self._rand_int(0, 2), 1 )
        elif (goalType == 3):
            goal_pos = (18 + self._rand_int(0, 2),20)

        self._goal_default_pos = goal_pos

        self._goal_default_pos = goal_pos
        
        # Generate the surrounding walls
        

        self.grid.horz_wall(4, 9, 13)
        self.grid.horz_wall(4, 12, 13)
        
        self.grid.vert_wall(4, 9, 3)

        self.grid.vert_wall(17, 0, 10)
        self.grid.vert_wall(17, 12, 10)

        self.grid.horz_wall(17, 0, 3)
        self.grid.horz_wall(17, 21, 3)
        self.grid.vert_wall(20, 0, 22)
        

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        
        self.mission = (
            "Get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        return obs, reward, done, info

class SimpleCorridor16x16(MiniGridEnv):
    

    def __init__(self, agent_pos=None, goal_pos=None, obstacle_type=None, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=16, max_steps=100)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)
        

        self._agent_default_pos = (6 + self._rand_int(0, 8), 7 + self._rand_int(0, 2))

        # random goal type
        goalType = self._rand_int(1, 4)
        
        self.goal_type = goalType

        if (goalType == 1):
            goal_pos = (1,7 + self._rand_int(0, 2))
        elif (goalType == 2):
            goal_pos = (13 + self._rand_int(0, 2), 1 )
        elif (goalType == 3):
            goal_pos = (13 + self._rand_int(0, 2),14)

        self._goal_default_pos = goal_pos

        self._goal_default_pos = goal_pos
        
        # Generate the surrounding walls
        

        self.grid.horz_wall(0, 6, 12)
        self.grid.horz_wall(0, 9, 12)
        
        self.grid.vert_wall(0, 6, 3)

        self.grid.vert_wall(12, 0, 7)
        self.grid.vert_wall(12, 9, 6)

        self.grid.horz_wall(12, 0, 3)
        self.grid.horz_wall(12, 15, 3)
        self.grid.vert_wall(15, 0, 16)
        

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        
        self.mission = (
            "Get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        return obs, reward, done, info

class Maze13x13(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment with lava to avoid.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=(6,7), goal_pos=None, obstacle_type=None, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=13, max_steps=100)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        types = ['lava']
        

        # random goal type
        goalType = random.randint(1,4)
        
        self.goal_type = goalType

        failure_pos = []

        failure_pos.append((7,11))
        failure_pos.append((10,8))

        if (goalType == 1):
            goal_pos = (4,3)
            
            failure_pos.append((9,3))
            failure_pos.append((5,9))
            failure_pos.append((9,9))

        elif (goalType == 2):
            goal_pos = (9,3)

            failure_pos.append((4,3))
            failure_pos.append((5,9))
            failure_pos.append((9,9))

        elif (goalType == 3):
            goal_pos = (5,9)

            failure_pos.append((4,3))
            failure_pos.append((9,3))
            failure_pos.append((9,9))

        elif (goalType == 4):
            goal_pos = (9,9)

            failure_pos.append((4,3))
            failure_pos.append((9,3))
            failure_pos.append((5,9))

        self._goal_default_pos = goal_pos
        self.failure_pos = failure_pos
        
        
        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        self.grid.horz_wall(2, 8, 5)
        self.grid.vert_wall(2, 8, 3)
        self.grid.vert_wall(4, 8, 3)
        self.grid.vert_wall(6, 8, 4)

        self.grid.horz_wall(2, 2, 4)
        self.grid.horz_wall(4, 4, 2)
        self.grid.horz_wall(2, 6, 5)
        self.grid.vert_wall(2, 2, 5)
        self.grid.vert_wall(5, 2, 3)
        self.grid.vert_wall(7, 1, 6)

        self.grid.horz_wall(9, 2, 2)
        self.grid.horz_wall(8, 4, 3)
        self.grid.vert_wall(8, 8, 4)
        self.grid.vert_wall(10, 8, 3)
        self.grid.vert_wall(10, 6, 1)

        self.grid.vert_wall(10, 2, 3)
        self.grid.vert_wall(9, 6, 3)
        
        

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # Generate and store random gap position
        self.gap_pos = np.array((
            self._rand_int(2, width - 2),
            self._rand_int(1, height - 1),
        ))

        ## Place the obstacle wall
        #self.grid.vert_wall(self.gap_pos[0], 1, height - 2, self.obstacle_type)
        
        # Put a hole in the wall
        #self.grid.set(self.gap_pos, self.obstacle_type)
        
        #self.mission = 'Reach the goal'
        
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        if tuple(self.agent_pos) in self.failure_pos:
            self.step_count += 10
        
        return obs, reward, done, info

class NineRoomsLavaEnv13x13(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment with lava to avoid.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=None, goal_pos=None, obstacle_type=Lava, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=13, max_steps=5000)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        types = ['lava']
        
        objs = []
        idx = 0

        # For each object to be generated
        # while len(objs) < self.numObjs:
        #     objType = self._rand_elem(types)
        #     objColor = self._rand_elem(COLOR_NAMES)

        #     if objType == 'key':
        #         obj = Key(objColor)
        #     elif objType == 'ball':
        #         obj = Ball(objColor)
        #     elif objType == 'lava':
        #         obj = Lava()

        #     self.place_obj(obj,top=(0, idx))
        #     objs.append(obj)
        #     idx += 1
        
        # random the number of lavas
        noOfLavas = random.randint(3,6)

        for i in range(0, noOfLavas):
            obj = Lava()
            self.put_obj(obj, random.randint(2,12), random.randint(2,12))
            idx += 1
        
        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 3
        room_h = height // 3

        # For each row of rooms
        for j in range(0, 3):

            # For each column
            for i in range(0, 3):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                hor = self._rand_int(yT + 1, yB)

                ver = self._rand_int(xL + 1, xR)
                # Bottom wall and door
                if i + 1 < 3:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, hor)
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 3:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (ver, yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # Generate and store random gap position
        self.gap_pos = np.array((
            self._rand_int(2, width - 2),
            self._rand_int(1, height - 1),
        ))

        ## Place the obstacle wall
        #self.grid.vert_wall(self.gap_pos[0], 1, height - 2, self.obstacle_type)
        
        # Put a hole in the wall
        #self.grid.set(self.gap_pos, self.obstacle_type)
        
        #self.mission = 'Reach the goal'
        
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        # print(obs)
        # print(reward)
        # print(done)
        # print(info)
        # print ("=======")
        
        return obs, reward, done, info

class FourRoomsLavaEnv11x11(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment with lava to avoid.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=(1,1), goal_pos=(9,9), obstacle_type=Lava, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=11, max_steps=1000)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        types = ['lava']
        
        objs = []
        idx = 0

        # For each object to be generated
        # while len(objs) < self.numObjs:
        #     objType = self._rand_elem(types)
        #     objColor = self._rand_elem(COLOR_NAMES)

        #     if objType == 'key':
        #         obj = Key(objColor)
        #     elif objType == 'ball':
        #         obj = Ball(objColor)
        #     elif objType == 'lava':
        #         obj = Lava()

        #     self.place_obj(obj,top=(0, idx))
        #     objs.append(obj)
        #     idx += 1
        
        # random the number of lavas
        noOfLavas = random.randint(1,4)

        for i in range(0, noOfLavas):
            obj = Lava()
            self.put_obj(obj, random.randint(2,9), random.randint(2,9))
            idx += 1
        
        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 2
        room_h = height // 2

        # For each row of rooms
        for j in range(0, 2):

            # For each column
            for i in range(0, 2):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                # Bottom wall and door
                if i + 1 < 2:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, yB // 2 + j + 1)
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 2:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (xR // 2 + i + 1, yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            #self.agent_pos = (1,1)
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
            #self.agent_dir = 1  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # Generate and store random gap position
        self.gap_pos = np.array((
            self._rand_int(2, width - 2),
            self._rand_int(1, height - 1),
        ))

        ## Place the obstacle wall
        #self.grid.vert_wall(self.gap_pos[0], 1, height - 2, self.obstacle_type)
        
        # Put a hole in the wall
        #self.grid.set(self.gap_pos, self.obstacle_type)
        
        #self.mission = 'Reach the goal'
        
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        # print(obs)
        # print(reward)
        # print(done)
        # print(info)
        # print ("=======")
        
        return obs, reward, done, info

class FourRoomsLavaEnv9x9(MiniGridEnv):
    """
    Classic 4 rooms gridworld environment with lava to avoid.
    Can specify agent and goal position, if not it set at random.
    """

    def __init__(self, agent_pos=(2,2), goal_pos=(6,6), obstacle_type=Lava, numObjs=4):
        self.obstacle_type = obstacle_type
        self._agent_default_pos = agent_pos
        self._goal_default_pos = goal_pos
        self.numObjs = numObjs
        
        super().__init__(grid_size=9, max_steps=1000)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        types = ['lava']
        
        objs = []
        idx = 0

        # For each object to be generated
        # while len(objs) < self.numObjs:
        #     objType = self._rand_elem(types)
        #     objColor = self._rand_elem(COLOR_NAMES)

        #     if objType == 'key':
        #         obj = Key(objColor)
        #     elif objType == 'ball':
        #         obj = Ball(objColor)
        #     elif objType == 'lava':
        #         obj = Lava()

        #     self.place_obj(obj,top=(0, idx))
        #     objs.append(obj)
        #     idx += 1
        
        # random the number of lavas
        noOfLavas = random.randint(1,2)

        for i in range(0, noOfLavas):
            obj = Lava()
            self.put_obj(obj, random.randint(2,7), random.randint(2,7))
            idx += 1
        
        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 2
        room_h = height // 2

        add = 0

        # For each row of rooms
        for j in range(0, 2):

            # For each column
            for i in range(0, 2):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                if (i == 1) or (j == 1):
                    add = 1
                else:
                    add = 0

                # Bottom wall and door
                if i + 1 < 2:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, yB // 2 + j + add)
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 2:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (xR // 2 + i + add, yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        if self._agent_default_pos is not None:
            self.agent_pos = self._agent_default_pos
            #self.agent_pos = (1,1)
            self.grid.set(*self._agent_default_pos, None)
            self.agent_dir = self._rand_int(0, 4)  # assuming random start direction
            #self.agent_dir = 1  # assuming random start direction
        else:
            self.place_agent()

        if self._goal_default_pos is not None:
            goal = Goal()
            self.put_obj(goal, *self._goal_default_pos)
            goal.init_pos, goal.cur_pos = self._goal_default_pos
        else:
            self.place_obj(Goal())

        # Generate and store random gap position
        self.gap_pos = np.array((
            self._rand_int(2, width - 2),
            self._rand_int(1, height - 1),
        ))

        ## Place the obstacle wall
        #self.grid.vert_wall(self.gap_pos[0], 1, height - 2, self.obstacle_type)
        
        # Put a hole in the wall
        #self.grid.set(self.gap_pos, self.obstacle_type)
        
        #self.mission = 'Reach the goal'
        
        self.mission = (
            "avoid the lava and get to the green goal square"
            if self.obstacle_type == Lava
            else "find the opening and get to the green goal square"
        )

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        
        # print(obs)
        # print(reward)
        # print(done)
        # print(info)
        # print ("=======")
        
        return obs, reward, done, info

register(
    id='MiniGrid-Customs-FourRooms-9x9-v0',
    entry_point='gym_minigrid.envs:FourRoomsEnv9x9'
)

register(
    id='MiniGrid-Customs-NineRoomsLava-16x16-v0',
    entry_point='gym_minigrid.envs:NineRoomsLavaEnv16x16'
)

register(
    id='MiniGrid-Customs-NineRoomsLava-13x13-v0',
    entry_point='gym_minigrid.envs:NineRoomsLavaEnv13x13'
)

register(
    id='MiniGrid-Customs-FourRoomsLava-11x11-v0',
    entry_point='gym_minigrid.envs:FourRoomsLavaEnv11x11'
)

register(
    id='MiniGrid-Customs-FourRoomsLava-9x9-v0',
    entry_point='gym_minigrid.envs:FourRoomsLavaEnv9x9'
)

register(
    id='MiniGrid-Customs-Maze-13x13-v0',
    entry_point='gym_minigrid.envs:Maze13x13'
)

register(
    id='MiniGrid-Customs-DoorKeyMaze-9x9-v0',
    entry_point='gym_minigrid.envs:DoorKeyMaze9x9'
)

register(
    id='MiniGrid-Customs-SimpleCorridor-v0',
    entry_point='gym_minigrid.envs:SimpleCorridor'
)

register(
    id='MiniGrid-Customs-SimpleCorridor16x16-v0',
    entry_point='gym_minigrid.envs:SimpleCorridor16x16'
)



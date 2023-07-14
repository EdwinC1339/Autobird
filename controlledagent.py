from autoagent import AutoAgent
from pygame import draw
import numpy as np


class ControlledAgent(AutoAgent):
    def __init__(self, margin):
        super().__init__()
        self.margin = margin

        # These could be passed to the agent but I'm choosing to copy them manually to avoid having to give the
        # controlled agent this data from the game scripts.
        self.pipe_v = -0.008
        self.gravity = 0.00061

        self.book_keep = (0, 0, 0, 0)
        self.target = 0
        self.encounter = 0

    def get_action(self, state):
        world_time, bird_y, bird_vy, a_p_x, a_p_y, i_p_x, i_p_y = state

        if world_time < 10:
            return False

        pipe_y = a_p_y if a_p_x > 0.06 else i_p_y

        self.book_keep = projected_position_idle, projected_position_jump, encounter_v_idle, encounter_v_jump \
            = self.predict(state)
        self.target = pipe_y

        if pipe_y > projected_position_jump + 0.08:
            # Definitely do not jump if jumping puts our projected position above the top pipe.
            return False

        d_idle = abs(projected_position_idle - pipe_y - 0.03)  # displacement from the goal if we choose not to jump
        d_jump = abs(projected_position_jump - pipe_y - 0.03)  # displacement from the goal if we choose to jump

        idle_in_margin = encounter_v_idle < self.margin
        jump_in_margin = encounter_v_jump < self.margin

        if idle_in_margin and jump_in_margin:
            # If both options yield acceptable velocities we can just choose the one with the smallest displacement
            return d_jump < d_idle
        elif idle_in_margin:
            # If jumping gives us too much velocity we stay idle
            return False
        elif jump_in_margin:
            # If staying idle accumulates too much acceleration due to gravity we jump
            return True
        else:
            # If both options are outside of the margin we just choose the one that gives better displacement (probably
            # will always jump here since acceleration is the only thing that causes this scenario)
            return d_jump < d_idle

    def predict(self, state):
        world_time, bird_y, bird_vy, a_p_x, a_p_y, i_p_x, i_p_y = state

        jump_vy = min(-0.011, bird_vy - 0.0085)

        # We only care about the pipe in front of us
        pipe_x = a_p_x if a_p_x > 0.06 else i_p_x
        self.encounter = pipe_x

        # The approach is where we would like our y to match the target y
        # When we get close to the pipe, this is just the moment our x will match the pipe's x
        # Otherwise it's some number of frames in the future
        t_pipe = (pipe_x - 0.3) / -self.pipe_v
        t_approach = np.clip(t_pipe, 4, 30)

        # Kinematics
        displacement_v = bird_vy * t_approach
        displacement_a = self.gravity * t_approach * t_approach / 2
        displacement_j = jump_vy * t_approach

        # Calculate velocity at encounter, if the velocity is too high then we discard the option. This is to avoid
        # high arcs where the bird would need to jump in the middle of the pipes.
        encounter_v_idle = abs(self.gravity * t_approach + bird_vy)
        encounter_v_jump = abs(self.gravity * t_approach + jump_vy)

        projected_position_idle = bird_y + displacement_v + displacement_a
        projected_position_jump = bird_y + displacement_j + displacement_a

        return projected_position_idle, projected_position_jump, encounter_v_idle, encounter_v_jump

    def draw_debug(self, surface, scale):
        projected_position_idle, projected_position_jump, encounter_v_idle, encounter_v_jump = self.book_keep
        draw.line(surface, "white",
                  (0, projected_position_idle * scale),
                  (scale, projected_position_idle * scale),
                  width=3)
        draw.line(surface, "yellow",
                  (0, projected_position_jump * scale),
                  (scale, projected_position_jump * scale),
                  width=3)

        draw.line(surface, "cyan",
                  (0, self.target * scale),
                  (scale, self.target * scale),
                  width=3)
        draw.line(surface, "cyan",
                  (self.encounter * scale, 0),
                  (self.encounter * scale, scale),
                  width=3)

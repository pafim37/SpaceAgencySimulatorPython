    import numpy as np

    class MoveBodyHandler:
        def move_planets2(self):
            for body in self.__bodies:
                dt = self.t
                if body.center_body_name == self.__barycentrum_name:
                    continue

                center_body = self.get_body_by_name(body.center_body_name)
                relative_position = body.get_relative_position_to(center_body)
                relative_velocity = body.get_relative_velocity_to(center_body)
                r = np.linalg.norm(relative_position)
                force = -self.__G * body.mass * center_body.mass * relative_position / r**3
                a = force / body.mass

                vel1_half = relative_velocity + 0.5 * dt * a
        
                pos = relative_position + dt * vel1_half
        
                a = -self.__G * center_body.mass * pos / np.linalg.norm(pos)**3
                
                vel1 = vel1_half + 0.5 * dt * a

                body.position = pos
                body.velocity = vel1
                self.t += 0.00001
        
        def move_body(self, body, center_body):
            state = np.array([body.position[0], body.position[1], body.position[2], body.velocity[0], body.velocity[1], body.velocity[2]])
            state += self.runge_kutta_4(state, body, center_body)
            position = np.array([state[0], state[1], state[2]])
            velocity = np.array([state[3], state[4], state[5]])
            body.position = position
            body.velocity = velocity

        def runge_kutta_4(self, state, body):
            t = self.t
            h = 0.0001
            k1 = self.two_body_problem(t + h, state, body, center_body)
            k2 = self.two_body_problem(t + h/2, state + k1/2, body, center_body)
            k3 = self.two_body_problem(t + h/2, state + k2/2, body, center_body)
            k4 = self.two_body_problem(t + h, state + k3, body, center_body)
            state = (k1 + 2*k2 + 2*k3 + k4) / 6
            self.t += h
            return state
                
        def two_body_problem(self, t, state, body, center_body):
            position = np.array([state[0], state[1], state[2]])
            velocity = np.array([state[3], state[4], state[5]])
            relative_position = body.get_relative_position_to(center_body)
            relative_velocity = body.get_relative_velocity_to(center_body)
            r = np.linalg.norm(relative_position)
            force = -self.__G * body.mass * center_body.mass * relative_position / r**3
            a = force / body.mass
            new_position = velocity * t + 0.5 * a * t**2
            new_velocity = a * t
            return np.array([new_position[0], new_position[1], new_position[2], new_velocity[0], new_velocity[1], new_velocity[2]])
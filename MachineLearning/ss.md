In the simplest terms, a policy maps each state to a single action.

The notation for a **deterministic policy** is:

$$\pi (s) = a$$

In other words, $\pi (s)$ represents the action selected in state $s$ by the policy $\pi$.

For example, $\pi$ may select the action $A_1$ in state $S_0$,  and action $A_1$ in states $S_1$ and $S_2$.

From this example we can see that an agent can select the same action in multiple states and some actions may not be selected in any state.

The notation for a **stochastic policy** is:

$$\pi (a|s)$$

This policy represents the probability of selecting action $a$ in state $s$.

A stochastic policy means there are multiple actions that may be selected with non-zero probability.

There are several basic rules for stochastic probabilities, these include:

-   The sum over all probability must be one for each state

$$\sum\limits_{a \in \mathscr{A}(s)} \pi (a|s) = 1$$

-   Each action probability must be non-negative

$$\pi (a|s) \geq 0$$

Another important point about policies is that they depend only on the current state, as opposed to other information like time or previous states.

In other words, in a Markov decision process the current state defines all the information used to select the current action.

In summary, an agents behavior in an environment is specified by a **policy** that maps the **current state** to a set of **probabilities for taking each action.** The policy also only depends on the current state.
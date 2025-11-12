# core/config.py

"""
Centralized configuration for the Spore simulation.

All constants and configuration values are defined here,
making it easy to adjust game balance and behavior.
"""

# =============================================================================
# WORLD CONFIGURATION
# =============================================================================

WORLD_START = 0
WORLD_END = 1000

# Prey can spawn anywhere from 0 to 1000 (as per assignment)
PREY_MIN_SPAWN = 0
PREY_MAX_SPAWN = 1000

# Maximum chase iterations (failsafe)
MAX_CHASE_ITERATIONS = 2000


# =============================================================================
# CREATURE EVOLUTION PARAMETERS
# =============================================================================

# Health ranges (same for both predator and prey)
MIN_HEALTH = 80
MAX_HEALTH = 120

# Base power ranges (same for both predator and prey)
MIN_POWER = 5
MAX_POWER = 15


# =============================================================================
# PREDATOR EVOLUTION PARAMETERS
# =============================================================================

# Predators need high stamina to chase prey over long distances
PREDATOR_MIN_STAMINA = 120
PREDATOR_MAX_STAMINA = 200

# Body part evolution chances (0.0 to 1.0)
PREDATOR_CHANCE_LEGS = 0.85  # High - need to run
PREDATOR_CHANCE_WINGS = 0.7  # High - helps catch prey
PREDATOR_CHANCE_CLAWS = 0.8  # High - for fighting
PREDATOR_CHANCE_TEETH = 0.7  # High - for fighting


# =============================================================================
# PREY EVOLUTION PARAMETERS
# =============================================================================

# Prey has less stamina but focuses on escape tactics
PREY_MIN_STAMINA = 40
PREY_MAX_STAMINA = 100

# Body part evolution chances (0.0 to 1.0)
PREY_CHANCE_LEGS = 0.85  # High - need to escape
PREY_CHANCE_WINGS = 0.5  # Moderate - good escape option
PREY_CHANCE_CLAWS = 0.3  # Low - not their focus
PREY_CHANCE_TEETH = 0.3  # Low - not their focus


# =============================================================================
# MOVEMENT SYSTEM CONFIGURATION
# =============================================================================

# Crawl (slowest, most efficient)
CRAWL_MIN_STAMINA = 0
CRAWL_STAMINA_COST = 1
CRAWL_SPEED = 1

# Hop (requires 1+ legs)
HOP_MIN_STAMINA = 20
HOP_STAMINA_COST = 2
HOP_SPEED = 3

# Walk (requires 2+ legs)
WALK_MIN_STAMINA = 40
WALK_STAMINA_COST = 2
WALK_SPEED = 4

# Run (requires 2+ legs)
RUN_MIN_STAMINA = 60
RUN_STAMINA_COST = 4
RUN_SPEED = 6

# Fly (requires 2+ wings, fastest)
FLY_MIN_STAMINA = 80
FLY_STAMINA_COST = 4
FLY_SPEED = 8


# =============================================================================
# SIMULATION CONFIGURATION
# =============================================================================

# Number of simulations to run
SIMULATION_COUNT = 100

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILENAME = "../logs/simulation.log"

# How often to log chase progress (every N turns)
CHASE_LOG_FREQUENCY = 10

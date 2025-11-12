# main.py

"""
Main entry point for the Spore simulation.
This script configures logging and runs the simulation 100 times.
"""

import logging
import sys
from spore.simulation import Simulation

# --- Constants ---
SIMULATION_COUNT = 100
LOG_LEVEL = logging.INFO  # Change to logging.DEBUG for more detail
LOG_FILENAME = "simulation.log"


def main() -> None:
    """Configures logging and runs all simulations."""

    # Get the root logger
    LOGGER = logging.getLogger()
    LOGGER.setLevel(LOG_LEVEL)

    # --- Setup Console Logging (what you see in the terminal) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    LOGGER.addHandler(console_handler)

    # --- Setup File Logging (what is saved to the file) ---
    # 'w' mode overwrites the file each time. Use 'a' to append.
    file_handler = logging.FileHandler(LOG_FILENAME, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Log EVERYTHING to the file
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    LOGGER.addHandler(file_handler)

    # Now, all LOGGER.info(), .warning(), etc. will go to BOTH places.

    LOGGER.info(f"Starting {SIMULATION_COUNT} simulations...")
    LOGGER.info(f"Full log output will be saved to {LOG_FILENAME}")

    sim_runner = Simulation()

    for i in range(SIMULATION_COUNT):
        LOGGER.info(
            # This line was shortened to be under 88 chars
            f"\n========== SIMULATION {i + 1}/{SIMULATION_COUNT} =========="
        )
        sim_runner.run()
        LOGGER.info(
            "=================================================\n"
        )

    LOGGER.info("All simulations complete.")


if __name__ == "__main__":
    main()
# runner/main.py

import logging
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import config
from core.simulation import Simulation


def setup_logging() -> logging.Logger:
    """
    Configure logging for the simulation.
    Creates both console and file handlers with appropriate
    formatting and log levels.
    Returns:
        The configured root logger
    """
    # Create logs directory if it doesn't exist
    log_path = Path(config.LOG_FILENAME)
    log_path.parent.mkdir(exist_ok=True)

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))

    # Clear any existing handlers
    logger.handlers.clear()

    # Console handler (what you see in terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (detailed log saved to file)
    file_handler = logging.FileHandler(config.LOG_FILENAME, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Save everything to file
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def main() -> None:
    """
    Main function: sets up logging and runs simulations.
    """
    logger = setup_logging()

    logger.info("=" * 70)
    logger.info(f"Starting {config.SIMULATION_COUNT} simulations...")
    logger.info(f"Full log output will be saved to {config.LOG_FILENAME}")
    logger.info("=" * 70)

    # Create simulation runner
    sim_runner = Simulation()

    # Track statistics

    # Run all simulations
    for i in range(config.SIMULATION_COUNT):
        logger.info("")
        logger.info(f"{'='*20} SIMULATION {i + 1}/{config.SIMULATION_COUNT} {'='*20}")

        sim_runner.run()
        # Track outcomes (you'd need to modify simulation.run() to return results)
        # For now, just separator
        logger.info("=" * 70)

    logger.info("")
    logger.info("=" * 70)
    logger.info("All simulations complete!")
    logger.info(f"Check {config.LOG_FILENAME} for detailed results")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()

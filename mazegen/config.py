from dataclasses import dataclass


@dataclass
class Config:
    """Store parsed maze configuration values."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


class ConfigParser:
    """Parse and validate maze configuration files."""

    REQUIRED_KEYS = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    def parse(self, filename: str) -> Config:
        """Parse a configuration file and return its values.

        Args:
            filename: Path to the configuration file.

        Returns:
            Validated maze configuration.

        Raises:
            ValueError: If the configuration is invalid.
        """
        values = self._read_file(filename)
        self._validate_required_keys(values)

        width = self._parse_int(values["WIDTH"], "WIDTH")
        height = self._parse_int(values["HEIGHT"], "HEIGHT")
        entry = self._parse_coordinates(
            values["ENTRY"],
            "ENTRY",
        )
        exit = self._parse_coordinates(
            values["EXIT"],
            "EXIT",
        )
        output_file = values["OUTPUT_FILE"]

        if not output_file:
            raise ValueError("OUTPUT_FILE cannot be empty")

        perfect = self._parse_bool(values["PERFECT"])
        seed = None
        if "SEED" in values:
            seed = self._parse_int(values["SEED"], "SEED")

        config = Config(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            output_file=output_file,
            perfect=perfect,
            seed=seed,
        )
        self._validate_config(config)
        return config

    def _read_file(
        self,
        filename: str,
    ) -> dict[str, str]:
        """Read configuration key-value pairs from a file."""
        values: dict[str, str] = {}

        try:
            with open(filename, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise ValueError(
                f"Configuration file not found: {filename}"
            )

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(
                    f"Invalid configuration line: {line}"
                )

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ValueError(
                    f"Configuration key cannot be empty: {line}"
                )
            if key in values:
                raise ValueError(
                    f"Duplicate configuration key: {key}"
                )

            values[key] = value

        return values

    def _validate_required_keys(
        self,
        values: dict[str, str],
    ) -> None:
        """Check whether all required configuration keys exist."""
        missing = self.REQUIRED_KEYS - values.keys()
        if missing:
            raise ValueError(
                "Missing configuration keys: "
                + ", ".join(sorted(missing))
            )

    def _parse_int(
        self,
        value: str,
        key: str,
    ) -> int:
        """Parse an integer configuration value."""
        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"{key} must be an integer: {value}"
            )

    def _parse_bool(self, value: str) -> bool:
        """Parse the PERFECT boolean configuration value."""
        if value == "True":
            return True
        if value == "False":
            return False
        raise ValueError(
            f"PERFECT must be True or False: {value}"
        )

    def _parse_coordinates(
        self,
        value: str,
        key: str,
    ) -> tuple[int, int]:
        """Parse coordinates written in x,y format."""
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError(
                f"{key} must have format x,y: {value}"
            )

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError:
            raise ValueError(
                f"{key} coordinates must be integers: {value}"
            )

        return (x, y)

    def _validate_config(
        self,
        config: Config,
    ) -> None:
        """Validate parsed maze configuration values."""
        if config.width <= 0:
            raise ValueError("WIDTH must be greater than 0")
        if config.height <= 0:
            raise ValueError("HEIGHT must be greater than 0")

        entry_x, entry_y = config.entry
        if not (
            0 <= entry_x < config.width
            and 0 <= entry_y < config.height
        ):
            raise ValueError(
                "ENTRY is outside maze bounds"
            )

        exit_x, exit_y = config.exit
        if not (
            0 <= exit_x < config.width
            and 0 <= exit_y < config.height
        ):
            raise ValueError(
                "EXIT is outside maze bounds"
            )

        if config.entry == config.exit:
            raise ValueError(
                "ENTRY and EXIT must be different"
            )

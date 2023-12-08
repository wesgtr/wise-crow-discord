from enums.medieval_fantasy import race_enum as medieval_race_enum, class_enum as medieval_class_enum
from enums.space_future import race_enum as space_race_enum, class_enum as space_class_enum
from enum import Enum


class EnvironmentEnum(Enum):
    MEDIEVAL_FANTASY = 1
    SPACE_FUTURE = 2


ENVIRONMENT_MAPPING = {
    EnvironmentEnum.MEDIEVAL_FANTASY.name: {
        'race': medieval_race_enum.RaceEnum,
        'class': medieval_class_enum.ClassEnum
    },
    EnvironmentEnum.SPACE_FUTURE.name: {
        'race': space_race_enum.RaceEnum,
        'class': space_class_enum.ClassEnum
    }
}

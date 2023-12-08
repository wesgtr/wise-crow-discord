from enum import Enum


class LanguageEnum(Enum):
    EN_US = (1, "en_US", "🇺🇸")
    PT_BR = (2, "pt_BR", "🇧🇷")
    # ZH_CN = (3, "zh_CN", "🇨🇳")
    # DE_DE = (4, "de_DE", "🇩🇪")
    # ES_ES = (5, "es_ES", "🇪🇸")

    @property
    def id(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @property
    def flag(self):
        return self.value[2]

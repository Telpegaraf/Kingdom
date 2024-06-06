class CharacterService:
    @staticmethod
    def check_change_stats(data, character, character_stats):
        if character.level == 1:
            if not all(value <= 18 for value in data.values()):
                return False
        new_stats_dict = dict(list(data.items())[:6])
        old_stats_sum = character_stats.strength + character_stats.dexterity + character_stats.constitution + \
                        character_stats.intelligence + character_stats.wisdom + character_stats.charisma
        new_stats_sum = sum(new_stats_dict.values())
        if new_stats_sum - old_stats_sum > character.stat_count:
            return False
        new_stat_count = character.stat_count - (new_stats_sum - old_stats_sum)
        character.stat_count = new_stat_count
        character.save()
        return True

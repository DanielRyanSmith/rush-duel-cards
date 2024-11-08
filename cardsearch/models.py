from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=200)
    card_type = models.CharField(max_length=200)
    card_property = models.CharField(max_length=50, null=True)
    japanese_name = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    image_url = models.CharField(max_length=1000)
    text = models.CharField(max_length=2000)
    effect_type = models.CharField(max_length=50, null=True)
    additional_text = models.CharField(max_length=1000, null=True)
    requirement = models.CharField(max_length=1000, null=True)
    effect = models.CharField(max_length=1000, null=True)

    monster_attribute = models.CharField(max_length=50, null=True)
    monster_level = models.IntegerField(default=0, null=True)
    monster_attack = models.IntegerField(null=True)
    monster_defense = models.IntegerField(null=True)

    def __str__(self):
        str_parts = [
            f"Name:        {self.name}",
            f"Type:        {self.card_type}",
            f"Property:    {self.card_property}",
            f"Status:      {self.status}",
        ]
        if self.monster_attribute is not None:
            str_parts.append(f"Attribute:   {self.monster_attribute}")
            str_parts.append(f"Level:       {self.monster_level}")
            str_parts.append(f"Attack:      {self.monster_attack}")
            str_parts.append(f"Defense:     {self.monster_defense}")
        if self.effect is None:
            str_parts.append(f"Text:\n{self.text}")
        else:
            str_parts.append("Text:")
            if self.additional_text is not None:
                str_parts.append(self.additional_text)
            str_parts.append(f"""[REQUIREMENT]
    {self.requirement}
[{self.effect_type}]
    {self.effect}""")
        
        return "\n".join(str_parts)


class MonsterType(models.Model):
    card = models.ForeignKey(
        'Card', related_name='monster_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

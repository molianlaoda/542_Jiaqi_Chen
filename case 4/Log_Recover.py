__author__ = 'Jiaqi'

from Operator import *

primary = Relation('data/cs542.db')
primary.open()
primary.back_up('data/cs542A.db')
primary.close()

primary.open()
primary.auto_increase()
primary.recover('data/cs542A.db')
primary.close()

secondary = Relation('data/cs542A.db')
secondary.open()
primary.open()
secondary.recover_show(primary)
primary.close()
secondary.close()



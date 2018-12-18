class Competition(models.Model):
	name = models.CharField(max_length=30)

class Event(models.Model):
	Competition_id = models.IntField()
	name = models.CharField(max_length=30)

class Student(models.Model):
	name = models.CharField(max_length=30)

class relation(models.Model):
	event_id = models.IntField()
	student_id = models.IntField()

class log(models.Model):
	student_name = models.CharField(max_length=30)
	competition_name = models.CharField(max_length=30)	
	timestamp = models.IntField()
	msg = models.CharField(max_length=255)

event_info = event.object.filter(name="test", Competition_id = '1')
relation_info = relation.object.filter(event_id=event_info[0].id)
student_info = {x.id: x for x in student.object.all()}
for x in relation_info:
	if x.student_id in student_info:
		print(student_info[x.id].name)
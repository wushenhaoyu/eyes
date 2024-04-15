from models import MedicalRecords
from models import Patient
from datetime import datetime

# 假设已经有一个 Patient 对象，可以通过 Patient.objects.get() 或其他方法获取
patient = Patient.objects.get(id=1)

# 创建一个 MedicalRecords 对象
medical_record = MedicalRecords(
    patient=patient,
    HospitalForTreatment="Hospital ABC",
    MedicalRecordTime=datetime.now(),
    MedicalRecordStatus=True,
    Picture='path/to/your/image.jpg',
    MedicalRecordResult="Some result"
)

# 保存对象到数据库
medical_record.save()

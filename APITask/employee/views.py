from .models import FEmployee, SEmployee, Job
from .serializer import FEmployeeSerializer, SEmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def add(request):
    job = Job.objects.create(name=f"JOB_{Job.objects.count() + 1}")

    data = request.data['file_data']

    femployees_to_create = []
    femployees_to_update = []
    semployees_to_create = []
    semployees_to_update = []

    for emp_data in data:
        fserializer = FEmployeeSerializer(data=emp_data)
        # sserializer = SEmployeeSerializer(data=emp_data)
        print(fserializer.is_valid())
        # print(sserializer.is_valid())

        if fserializer.is_valid():  # and sserializer.is_valid():
            try:
                femployee = FEmployee.objects.get(id=emp_data['id'])
                valid_object = fserializer.update(femployee, fserializer.validated_data, job=job)
                femployees_to_update.append(valid_object)
            except FEmployee.DoesNotExist:
                valid_object = fserializer.create(fserializer.validated_data, job=job)
                femployees_to_create.append(valid_object)

            # try:
            #     semployee = SEmployee.objects.get(id=emp_data['id'])
            #     valid_object = sserializer.update(semployee, sserializer.validated_data, job=job)
            #     semployees_to_update.append(valid_object)
            # except SEmployee.DoesNotExist:
            #     valid_object = sserializer.create(sserializer.validated_data, job=job)
            #     semployees_to_create.append(valid_object)
        else:
            return Response({
                'status': 'Failure',
                'message': fserializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
    print(femployees_to_create[0].source)
    print(femployees_to_update[0].source)
    # print(semployees_to_create)
    # print(semployees_to_update)
    
    if femployees_to_create:
        FEmployee.objects.bulk_create([FEmployee(data) for data in femployees_to_create])
    if femployees_to_update:
        FEmployee.objects.bulk_update(femployees_to_update, ['name', 'email', 'mobile', 'department', 'designation', 'source'])

    # if semployees_to_create:
    #     SEmployee.objects.bulk_create([SEmployee(data) for data in semployees_to_create])
    # if semployees_to_update:
    #     SEmployee.objects.bulk_update(semployees_to_update, ['name', 'email', 'mobile', 'department', 'salary', 'source'])
    
    job.status = 'Success'
    job.save()
    return Response({'status': 'success', 'message': 'Data Operation Successful'}, status=status.HTTP_200_OK)

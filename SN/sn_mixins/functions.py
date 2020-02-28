
def upload_location(instance, filename):
    """
    instance.__class__ gets the model Post. We must use this
    method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    U Can Try:
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    """
    model_inst = instance.__class__
    # print(model_inst)
    new_id = model_inst.objects.order_by("id").last().id + 1 \
        if model_inst.objects.exists() else 1

    # print( f'{instance.__class__.__name__}/{new_id}/{filename}')
    return f'{instance.__class__.__name__}/{new_id}/{filename}'
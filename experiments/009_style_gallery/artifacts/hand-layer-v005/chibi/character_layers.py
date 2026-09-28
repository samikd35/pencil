"""Correct front-arm occlusion in the demonstrated three-pass Pencil character setup."""
import bpy


def separate_front_arm():
    scene=bpy.context.scene
    tree=scene.compositing_node_group
    required=('Stage and limbs','Unified body','Face')
    renders={node.layer:node for node in tree.nodes if node.type=='R_LAYERS'}
    if not all(name in renders for name in required):
        raise ValueError('Front-arm correction expects the existing stage/body/face compositor')
    if 'Front arm' in scene.view_layers:
        raise ValueError('Front-arm layers already exist; revise the saved controls instead of applying twice')
    front=bpy.data.collections.new('Foreground arm artwork')
    hand=bpy.data.collections.new('Foreground hand artwork')
    for collection in (front,hand):scene.collection.children.link(collection)
    def move(obj,collection):
        for old in list(obj.users_collection):old.objects.unlink(obj)
        collection.objects.link(obj)
    for name in ('Arm_near','Arm_near fill'):move(bpy.data.objects[name],front)
    for name in ('Mitten_near','Mitten_near_outline'):move(bpy.data.objects[name],hand)
    # A sleeve belongs with its arm. Leaving it in the torso pass makes the arm cover its cuff.
    for name in ('STYLE sleeve near','Short sleeve near','Captain band'):
        obj=bpy.data.objects.get(name)
        if obj is None:continue
        move(obj,front)
        if 'sleeve' in name:
            border=obj.copy();border.data=obj.data.copy();border.name='Foreground sleeve outline'
            border.data.bevel_depth+=.016;border.location.z-=.025
            border.data.materials.clear();border.data.materials.append(bpy.data.objects['Arm_near'].data.materials[0])
            front.objects.link(border)
    new_names={front.name,hand.name}
    for layer in scene.view_layers:
        for child in layer.layer_collection.children:
            if child.name in new_names:child.exclude=True
    for name,collection in (('Front arm',front),('Front hand',hand)):
        layer=scene.view_layers.new(name)
        for child in layer.layer_collection.children:
            child.exclude=child.name not in (collection.name,'Pose controls • keyed and editable')
        node=tree.nodes.new('CompositorNodeRLayers');node.layer=name;renders[name]=node
    nodes=tree.nodes;links=tree.links
    border=next(n for n in nodes if n.type=='SETALPHA')
    glare=next(n for n in nodes if n.type=='GLARE')
    def over(background,foreground):
        node=nodes.new('CompositorNodeAlphaOver');node.label='Front-arm correction'
        links.new(background,node.inputs['Background']);links.new(foreground,node.inputs['Foreground'])
        return node.outputs[0]
    body=over(renders['Stage and limbs'].outputs['Image'],border.outputs[0])
    body=over(body,renders['Unified body'].outputs['Image'])
    below_face=over(over(body,renders['Front arm'].outputs['Image']),renders['Face'].outputs['Image'])
    above_face=over(over(body,renders['Face'].outputs['Image']),renders['Front arm'].outputs['Image'])
    mix=nodes.new('ShaderNodeMix');mix.data_type='RGBA';mix.label='Front arm in front of face (pose control)'
    links.new(below_face,mix.inputs[6]);links.new(above_face,mix.inputs[7])
    scene['front_arm_over_face']=0.0
    scene.id_properties_ui('front_arm_over_face').update(min=0,max=1,description='Key 0/1 with constant interpolation to place the near arm below/above the face; no motion changes')
    curve=mix.inputs[0].driver_add('default_value');variable=curve.driver.variables.new()
    variable.name='order';variable.type='SINGLE_PROP';variable.targets[0].id_type='SCENE'
    variable.targets[0].id=scene;variable.targets[0].data_path='["front_arm_over_face"]';curve.driver.expression='order'
    image=over(mix.outputs[2],renders['Front hand'].outputs['Image'])
    links.new(image,glare.inputs['Image'])
    # The stage pass now excludes the near arm. Evaluate/edit geometry in an all-artwork
    # layer; a stage-only dependency graph otherwise returns unevaluated arm coordinates.
    editing=scene.view_layers.new('Character editing');editing.use=False
    bpy.context.window.view_layer=editing
    scene['Arm layering']='Far arm behind body; near arm in front of body; near hand in front of face. front_arm_over_face is an independent pose-order control.'
    return [o.name for o in front.objects], [o.name for o in hand.objects]

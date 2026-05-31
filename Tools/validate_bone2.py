import unreal
L = lambda s: unreal.log(f"[B2] {s}")
unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
ANIM = unreal.load_asset("/Game/Alice/AnimM/A_Walk")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
sk = unreal.load_asset("/Game/Alice/Characters/AliceVestido/SK_AliceVestido")
actor = eas.spawn_actor_from_class(unreal.SkeletalMeshActor, unreal.Vector(0,0,0))
comp = actor.skeletal_mesh_component
comp.set_skeletal_mesh_asset(sk)
comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
comp.set_animation(ANIM)

# usa nomes reais (apareceram: Hips, Spine, Spine1...). pega bones de perna que mais mexem no walk
n = comp.get_num_bones()
allnames = [str(comp.get_bone_name(i)) for i in range(n)]
L(f"bones[10..20]={allnames[10:20]}")

def boneloc(name, t):
    comp.set_position(t, True)
    try:
        return comp.get_bone_transform(name).translation
    except Exception:
        return None

# testa por NOME direto
def dist(a,b):
    return ((a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2)**0.5
maxd = 0.0; best=None
for bn in allnames:
    a = boneloc(bn, 0.0); b = boneloc(bn, 0.6)
    if a and b:
        d = dist(a,b)
        if d>maxd: maxd=d; best=bn
L(f">>> bone que mais moveu: {best} delta={maxd:.2f}")
L(f">>> {'ANIMA OK (pesos+anim funcionam)' if maxd>0.5 else 'PARADO (anim nao avalia)'}")
eas.destroy_actor(actor)
L("END")

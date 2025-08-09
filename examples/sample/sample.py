import animator.animation

sample_assets = "examples/sample/assets"
sample_instructions = "examples/sample/animation.json"
anim = animator.animation.Animation(sample_assets, sample_instructions, canvas_size=(640, 480), fps=30)
print(anim.summary())
anim.export("examples/sample/output.mp4")
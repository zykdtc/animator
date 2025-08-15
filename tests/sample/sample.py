import animator.animation

sample_assets = "tests/sample/assets"
sample_instructions = "tests/sample/animation.json"
anim = animator.animation.Animation(sample_assets, sample_instructions, canvas_size=(640, 480), fps=30)
print(anim.summary())
anim.export("tests/sample/output.mp4")
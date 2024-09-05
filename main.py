from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()  # Ursina 애플리케이션을 시작합니다.

jump_height = 2  # 점프 높이 설정 (기본값: 2)
jump_duration = 0.5  # 점프 지속 시간 설정 (기본값: 0.5)
jump_fall_after = 0.35  # 점프 후 낙하 시작 시간 설정 (기본값: 0.35)
gravity_scale = 1  # 중력 스케일 설정 (기본값: 1)
mouse_sensitivity = Vec2(40,40)  # 마우스 감도 설정 (기본값: (40,40))
run_speed = 5  # 이동 속도 설정 (기본값: 5)

window.fps_counter.enabled = False  # FPS 카운터 비활성화
window.exit_button.visible = False  # 종료 버튼 숨김

punch = Audio('punch', autoplay=False)  # 'punch' 오디오 객체 생성

blocks = [
    load_texture('grass.png'),  # 0 - 잔디 텍스처
    load_texture('grass.png'),  # 1 - 잔디 텍스처
    load_texture('stone.png'),  # 2 - 돌 텍스처
    load_texture('gold.png'),   # 3 - 금 텍스처
    load_texture('lava.png'),   # 4 - 용암 텍스처
]

block_id = 1  # 현재 선택된 블록 ID

def input(key):
    global block_id, hand
    if key.isdigit():  # 숫자 키를 눌렀을 때
        block_id = int(key)  # 블록 ID 업데이트
        if block_id >= len(blocks):  # 블록 ID가 리스트 길이를 초과하면
            block_id = len(blocks) - 1  # 최대 인덱스로 설정
        hand.texture = blocks[block_id]  # 손의 텍스처를 현재 블록 텍스처로 변경



sky = Entity(
    parent=scene,  # 씬의 자식으로 추가
    model='sphere',  # 구 모델 사용
    texture=load_texture('sky.jpg'),  # 하늘 텍스처
    scale=500,  # 구의 크기
    double_sided=True  # 양면 렌더링
)

hand = Entity(
    parent=camera.ui,  # 카메라 UI의 자식으로 추가
    model='block',  # 블록 모델 사용
    texture=blocks[block_id],  # 현재 블록 텍스처
    scale=0.2,  # 손 크기
    rotation=Vec3(-10, -10, 10),  # 손 회전
    position=Vec2(0.6, -0.6)  # 손 위치
)

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:  # 마우스 왼쪽 또는 오른쪽 버튼이 눌려졌을 때
        punch.play()  # 'punch' 소리 재생
        hand.position = Vec2(0.4, -0.5)  # 손의 위치를 변경
    else:
        hand.position = Vec2(0.6, -0.6)  # 손의 위치를 원래대로 되돌림



class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass.png'):
        super().__init__(
            parent=scene,  # 씬의 자식으로 추가
            position=position,  # 블록 위치
            model='block',  # 블록 모델 사용
            origin_y=0.5,  # 원점 위치 설정
            texture=texture,  # 블록 텍스처
            color=color.color(0, 0, random.uniform(0.9, 1.0)),  # 블록 색상
            scale=0.5  # 블록 크기
        )

    def input(self, key):
        if self.hovered:  # 블록에 마우스 커서가 있을 때
            if key == 'left mouse down':  # 왼쪽 마우스 버튼 클릭
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])  # 새로운 블록 추가
            elif key == 'right mouse down':  # 오른쪽 마우스 버튼 클릭
                destroy(self)  # 블록 삭제

                

for z in range(20):  # z축을 따라 반복
    for x in range(20):  # x축을 따라 반복
        voxel = Voxel(position=(x, 0, z))  # 블록 생성

player = FirstPersonController()  # 1인칭 컨트롤러 생성

player.jump_height = jump_height  # 점프 높이 설정
player.jump_up_duration = jump_duration  # 점프 지속 시간 설정
player.mouse_sensitivity = mouse_sensitivity  # 마우스 감도 설정
player.speed = run_speed  # 이동 속도 설정
player.gravity = gravity_scale  # 중력 설정

app.run()  # 애플리케이션 실행

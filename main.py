"""
LunarGuard — Sistema de Monitoramento Visual de Base Lunar
FIAP Global Solution 2025 — Space Connect

Uso:
    python main.py               # webcam padrão
    python main.py --source 1    # segunda câmera
    python main.py --source video.mp4   # arquivo de vídeo

Teclas:
    Q  — sair
    R  — resetar background subtractor (útil ao mudar cena)
    Z  — mostrar/ocultar zonas
"""

import argparse
import time
import cv2

from detector.motion import MotionDetector
from detector.zone   import ZoneManager
from detector.pose   import FallDetector
from ui.overlay      import Overlay


def parse_args():
    parser = argparse.ArgumentParser(description="LunarGuard — Monitoramento Visual")
    parser.add_argument(
        "--source", default="0",
        help="Índice da câmera (0, 1, ...) ou caminho de vídeo. Padrão: 0",
    )
    return parser.parse_args()


def open_capture(source: str):
    src = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir a fonte de vídeo: {source}")
    return cap


def main():
    args = parse_args()
    cap  = open_capture(args.source)

    # Obtém dimensões reais do frame
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Inicializa módulos
    motion_detector = MotionDetector(min_area=1500)
    zone_manager    = ZoneManager(frame_w, frame_h)
    fall_detector   = FallDetector()
    overlay         = Overlay()

    show_zones = True

    # Controle de FPS
    prev_time = time.time()

    # Cooldown de alertas para não disparar a cada frame
    last_fall_alert      = 0.0
    last_intrusion_alert = 0.0
    ALERT_COOLDOWN       = 4.0   # segundos entre alertas do mesmo tipo

    print("[LunarGuard] Iniciando... Pressione Q para sair, R para resetar, Z para zonas.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[LunarGuard] Fim do vídeo ou câmera desconectada.")
            break

        # ── Pré-processamento ─────────────────────────────────────────
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # ── Detecções ─────────────────────────────────────────────────
        motion_boxes = motion_detector.detect(frame)
        intrusions   = zone_manager.check_intrusion(motion_boxes)
        fall_detected = fall_detector.process(frame_rgb)

        # ── Disparar alertas (com cooldown) ───────────────────────────
        now = time.time()

        if fall_detected and (now - last_fall_alert) > ALERT_COOLDOWN:
            overlay.trigger_alert("ASTRONAUTA CAIDO / COLAPSO DETECTADO", duration=3.0)
            last_fall_alert = now

        if intrusions and (now - last_intrusion_alert) > ALERT_COOLDOWN:
            zone_names = ", ".join({z.name for z, _ in intrusions})
            overlay.trigger_alert(f"INTRUSAO EM ZONA RESTRITA: {zone_names}", duration=3.0)
            last_intrusion_alert = now

        # ── Desenho ───────────────────────────────────────────────────
        if show_zones:
            overlay.draw_zones(frame, zone_manager.zones)

        overlay.draw_motion_boxes(frame, motion_boxes)
        overlay.draw_pose(frame, fall_detector.landmarks)

        # FPS
        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-9)
        prev_time = curr_time

        overlay.draw_hud(
            frame,
            status="",
            fps=fps,
            fall=fall_detected,
            intrusion=bool(intrusions),
        )
        overlay.draw_alert(frame)

        cv2.imshow("LunarGuard — Base Lunar Monitoring System", frame)

        # ── Teclas ────────────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            motion_detector = MotionDetector(min_area=1500)
            print("[LunarGuard] Background subtractor resetado.")
        elif key == ord("z"):
            show_zones = not show_zones

    # Limpeza
    cap.release()
    fall_detector.close()
    cv2.destroyAllWindows()
    print("[LunarGuard] Encerrado.")


if __name__ == "__main__":
    main()

# encoding: utf-8
import os
import shutil
import glob
from pretty_midi import PrettyMIDI, ControlChange
import pdb

"""
同じフォルダにある.midのパートMIDI、オールMIDIを生成し、outディレクトリ(存在しない場合は作る)に出力する
mainSound, subSound : 楽器種類
volumns : MIDIのパート数と一致するとボリュームがこれになる
volumeDiff : パートMIDIの該当パートを大きくする
namse : MIDIにパート名情報がなくてかつパート数が一致するときに使用される
"""

mainSound = 68
subSound = 11    
volumes = [95, 99, 102, 108]
volumeDiff = 20
names = ["sop", "alt", "ten", "bas"]

def part_midi(f, key=None):
    fname = f.split(os.path.sep)[-1]
    _midi = PrettyMIDI(f)
    # part
    for ind, instrument in enumerate(_midi.instruments):
        midi = PrettyMIDI(f)
        n = len(midi.instruments)
        # sound
        for ind2, inst in enumerate(midi.instruments):
            if ind2 != ind:
                inst.program = subSound
            else:
                inst.program = mainSound
        if instrument.name:
            name = instrument.name 
        elif len(names)==n:
            name = names[ind]
        else:
            name = str(ind)
        if n!=len(volumes):
            continue
        # volume
        for inst, value in zip(midi.instruments, volumes):
            if instrument is inst:
                value += volumeDiff
            inst.control_changes.append(ControlChange(number=7, value=value, time=0.001))
        midi.write(os.path.join(outdir, fname.rsplit(".",1)[0] + "_" + name + ".mid"))
def all_midi(f, key=None):
    midi = PrettyMIDI(f)
    fname = f.split(os.path.sep)[-1]
    n = len(midi.instruments)
    for ind, instrument in enumerate(midi.instruments):
        # sound
        instrument.program = mainSound
        if n==len(volumes):
            instrument.control_changes.append(ControlChange(number=7, value=volumes[ind], time=0.001))
    midi.write(os.path.join(outdir, fname.rsplit(".",1)[0] + "_all.mid"))

if __name__=="__main__":
    files = glob.glob(os.path.join(os.path.dirname(__file__), "*.mid"))
    # files = glob.glob(os.path.join(os.path.dirname(__file__), "*.MID"))
    if files:
        print("{} file found".format(len(files)))
        outdir = os.path.join(os.path.dirname(__file__), "out")
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    for f in files:
        part_midi(f)
        all_midi(f)
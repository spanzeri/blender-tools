# sams-blender-tools

A collection of awful tools I quickly put together for personal use.

None of those are particularly good or generic, this is just a place where I might or might not add addons I write from time to time.

**Use at your personal risk**

Most of those plugins are developed as helpers for the rigging and animation worflow from the [P2Design curses](https://www.p2design.com/courses/) (in particular "The art of Effective Rigging).

## Create target bones

It iterates over every bone on armature.

For every "deformation" bone, it creates a corresponding TGT-<bone_name> bone in the last layer.

It also adds a copy transform constraint on the original bone to the new TGT bone.

## Root properties

This plugin is meant to work in tandem with [Bone Manager](https://fin.gumroad.com/l/STdb).

It adds a new panel in the "Bone Layer" section that displays all the custom properties for bones with a specific name in the armature.

Possible bone names are:
 - Root, ROOT, root
 - Props, PROPS, props
 - Properties, properties, PROPERTIES

This is useful for rigs that use custom properties as drivers, because it allows to have quick access (and edit) of those values without having to select the right bone and dig down in the inspector.

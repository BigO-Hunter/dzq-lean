// Lean compiler output
// Module: Z2FORM
// Imports: public import Init public meta import Init public import Mathlib.Tactic
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lp_mathlib_Nat_cast___at___00Mathlib_Meta_NormNum_evalRealSqrt_spec__3(lean_object*);
lean_object* l_Rat_pow(lean_object*, lean_object*);
lean_object* l_Rat_mul(lean_object*, lean_object*);
lean_object* l_Rat_sub(lean_object*, lean_object*);
lean_object* l_Rat_add(lean_object*, lean_object*);
static lean_once_cell_t lp_dzq_x2dlean_x2dformal_zW___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_dzq_x2dlean_x2dformal_zW___closed__0;
static lean_once_cell_t lp_dzq_x2dlean_x2dformal_zW___closed__1_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_dzq_x2dlean_x2dformal_zW___closed__1;
static lean_once_cell_t lp_dzq_x2dlean_x2dformal_zW___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_dzq_x2dlean_x2dformal_zW___closed__2;
LEAN_EXPORT lean_object* lp_dzq_x2dlean_x2dformal_zW(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_dzq_x2dlean_x2dformal_zL___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_dzq_x2dlean_x2dformal_zL___closed__0;
LEAN_EXPORT lean_object* lp_dzq_x2dlean_x2dformal_zL(lean_object*, lean_object*, lean_object*);
static lean_object* _init_lp_dzq_x2dlean_x2dformal_zW___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(7u);
v___x_2_ = lp_mathlib_Nat_cast___at___00Mathlib_Meta_NormNum_evalRealSqrt_spec__3(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_dzq_x2dlean_x2dformal_zW___closed__1(void){
_start:
{
lean_object* v___x_3_; lean_object* v___x_4_; 
v___x_3_ = lean_unsigned_to_nat(5u);
v___x_4_ = lp_mathlib_Nat_cast___at___00Mathlib_Meta_NormNum_evalRealSqrt_spec__3(v___x_3_);
return v___x_4_;
}
}
static lean_object* _init_lp_dzq_x2dlean_x2dformal_zW___closed__2(void){
_start:
{
lean_object* v___x_5_; lean_object* v___x_6_; 
v___x_5_ = lean_unsigned_to_nat(2u);
v___x_6_ = lp_mathlib_Nat_cast___at___00Mathlib_Meta_NormNum_evalRealSqrt_spec__3(v___x_5_);
return v___x_6_;
}
}
LEAN_EXPORT lean_object* lp_dzq_x2dlean_x2dformal_zW(lean_object* v_x1_7_, lean_object* v_x2_8_, lean_object* v_x3_9_){
_start:
{
lean_object* v___x_10_; lean_object* v___x_11_; lean_object* v___x_12_; lean_object* v___x_13_; lean_object* v___x_14_; lean_object* v___x_15_; lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; lean_object* v___x_19_; lean_object* v___x_20_; lean_object* v___x_21_; lean_object* v___x_22_; lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; lean_object* v___x_27_; 
v___x_10_ = lean_obj_once(&lp_dzq_x2dlean_x2dformal_zW___closed__0, &lp_dzq_x2dlean_x2dformal_zW___closed__0_once, _init_lp_dzq_x2dlean_x2dformal_zW___closed__0);
v___x_11_ = lean_obj_once(&lp_dzq_x2dlean_x2dformal_zW___closed__1, &lp_dzq_x2dlean_x2dformal_zW___closed__1_once, _init_lp_dzq_x2dlean_x2dformal_zW___closed__1);
lean_inc_ref(v_x1_7_);
v___x_12_ = l_Rat_mul(v___x_11_, v_x1_7_);
v___x_13_ = l_Rat_add(v___x_10_, v___x_12_);
v___x_14_ = lean_unsigned_to_nat(2u);
v___x_15_ = l_Rat_pow(v_x1_7_, v___x_14_);
v___x_16_ = l_Rat_mul(v___x_11_, v___x_15_);
v___x_17_ = l_Rat_sub(v___x_13_, v___x_16_);
v___x_18_ = lean_obj_once(&lp_dzq_x2dlean_x2dformal_zW___closed__2, &lp_dzq_x2dlean_x2dformal_zW___closed__2_once, _init_lp_dzq_x2dlean_x2dformal_zW___closed__2);
lean_inc_ref(v_x2_8_);
v___x_19_ = l_Rat_pow(v_x2_8_, v___x_14_);
v___x_20_ = l_Rat_mul(v___x_18_, v___x_19_);
v___x_21_ = l_Rat_sub(v___x_17_, v___x_20_);
v___x_22_ = l_Rat_mul(v___x_18_, v_x2_8_);
lean_inc_ref(v_x3_9_);
v___x_23_ = l_Rat_mul(v___x_22_, v_x3_9_);
lean_dec_ref(v___x_22_);
v___x_24_ = l_Rat_sub(v___x_21_, v___x_23_);
v___x_25_ = l_Rat_pow(v_x3_9_, v___x_14_);
v___x_26_ = l_Rat_mul(v___x_18_, v___x_25_);
v___x_27_ = l_Rat_add(v___x_24_, v___x_26_);
return v___x_27_;
}
}
static lean_object* _init_lp_dzq_x2dlean_x2dformal_zL___closed__0(void){
_start:
{
lean_object* v___x_28_; lean_object* v___x_29_; 
v___x_28_ = lean_unsigned_to_nat(1u);
v___x_29_ = lp_mathlib_Nat_cast___at___00Mathlib_Meta_NormNum_evalRealSqrt_spec__3(v___x_28_);
return v___x_29_;
}
}
LEAN_EXPORT lean_object* lp_dzq_x2dlean_x2dformal_zL(lean_object* v_x1_30_, lean_object* v_x2_31_, lean_object* v_x3_32_){
_start:
{
lean_object* v___x_33_; lean_object* v___x_34_; lean_object* v___x_35_; lean_object* v___x_36_; lean_object* v___x_37_; lean_object* v___x_38_; lean_object* v___x_39_; lean_object* v___x_40_; lean_object* v___x_41_; lean_object* v___x_42_; lean_object* v___x_43_; lean_object* v___x_44_; lean_object* v___x_45_; lean_object* v___x_46_; lean_object* v___x_47_; lean_object* v___x_48_; lean_object* v___x_49_; 
v___x_33_ = lean_unsigned_to_nat(2u);
lean_inc_ref_n(v_x1_30_, 2);
v___x_34_ = l_Rat_pow(v_x1_30_, v___x_33_);
v___x_35_ = lean_obj_once(&lp_dzq_x2dlean_x2dformal_zL___closed__0, &lp_dzq_x2dlean_x2dformal_zL___closed__0_once, _init_lp_dzq_x2dlean_x2dformal_zL___closed__0);
v___x_36_ = lean_obj_once(&lp_dzq_x2dlean_x2dformal_zW___closed__2, &lp_dzq_x2dlean_x2dformal_zW___closed__2_once, _init_lp_dzq_x2dlean_x2dformal_zW___closed__2);
v___x_37_ = l_Rat_mul(v___x_36_, v_x1_30_);
v___x_38_ = l_Rat_sub(v___x_35_, v___x_37_);
lean_inc_ref(v___x_38_);
v___x_39_ = l_Rat_mul(v_x1_30_, v___x_38_);
lean_dec_ref(v_x1_30_);
v___x_40_ = l_Rat_add(v___x_34_, v___x_39_);
v___x_41_ = l_Rat_pow(v___x_38_, v___x_33_);
v___x_42_ = l_Rat_sub(v___x_40_, v___x_41_);
lean_inc_ref(v_x2_31_);
v___x_43_ = l_Rat_pow(v_x2_31_, v___x_33_);
lean_inc_ref(v_x3_32_);
v___x_44_ = l_Rat_mul(v_x2_31_, v_x3_32_);
lean_dec_ref(v_x2_31_);
v___x_45_ = l_Rat_add(v___x_43_, v___x_44_);
v___x_46_ = l_Rat_pow(v_x3_32_, v___x_33_);
v___x_47_ = l_Rat_sub(v___x_45_, v___x_46_);
v___x_48_ = l_Rat_mul(v___x_36_, v___x_47_);
v___x_49_ = l_Rat_sub(v___x_42_, v___x_48_);
return v___x_49_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic(uint8_t builtin);
void lean_initialize();
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_dzq_x2dlean_x2dformal_Z2FORM(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
lean_initialize();
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif

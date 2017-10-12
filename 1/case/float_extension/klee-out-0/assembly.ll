; ModuleID = 'float_extension_i.bc'
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%"class.std::ios_base::Init" = type { i8 }
%"class.std::basic_ostream" = type { i32 (...)**, %"class.std::basic_ios" }
%"class.std::basic_ios" = type { %"class.std::ios_base", %"class.std::basic_ostream"*, i8, i8, %"class.std::basic_streambuf"*, %"class.std::ctype"*, %"class.std::num_put"*, %"class.std::num_get"* }
%"class.std::ios_base" = type { i32 (...)**, i64, i64, i32, i32, i32, %"struct.std::ios_base::_Callback_list"*, %"struct.std::ios_base::_Words", [8 x %"struct.std::ios_base::_Words"], i32, %"struct.std::ios_base::_Words"*, %"class.std::locale" }
%"struct.std::ios_base::_Callback_list" = type { %"struct.std::ios_base::_Callback_list"*, void (i32, %"class.std::ios_base"*, i32)*, i32, i32 }
%"struct.std::ios_base::_Words" = type { i8*, i64 }
%"class.std::locale" = type { %"class.std::locale::_Impl"* }
%"class.std::locale::_Impl" = type { i32, %"class.std::locale::facet"**, i64, %"class.std::locale::facet"**, i8** }
%"class.std::locale::facet" = type { i32 (...)**, i32 }
%"class.std::basic_streambuf" = type { i32 (...)**, i8*, i8*, i8*, i8*, i8*, i8*, %"class.std::locale" }
%"class.std::ctype" = type { %"class.std::locale::facet", %struct.__locale_struct*, i8, i32*, i32*, i16*, i8, [256 x i8], [256 x i8], i8 }
%struct.__locale_struct = type { [13 x %struct.__locale_data*], i16*, i32*, i32*, [13 x i8*] }
%struct.__locale_data = type opaque
%"class.std::num_put" = type { %"class.std::locale::facet" }
%"class.std::num_get" = type { %"class.std::locale::facet" }
%"struct.std::_Setprecision" = type { i32 }

@_ZStL8__ioinit = internal global %"class.std::ios_base::Init" zeroinitializer, align 1
@__dso_handle = external global i8
@.str = private unnamed_addr constant [2 x i8] c"x\00", align 1
@.str1 = private unnamed_addr constant [4 x i8] c"res\00", align 1
@_ZSt4cout = external global %"class.std::basic_ostream"
@llvm.global_ctors = appending global [1 x { i32, void ()* }] [{ i32, void ()* } { i32 65535, void ()* @_GLOBAL__I_a }]
@.str2 = private unnamed_addr constant [67 x i8] c"/home/walker/Projects/klee/runtime/Intrinsic/klee_div_zero_check.c\00", align 1
@.str13 = private unnamed_addr constant [15 x i8] c"divide by zero\00", align 1
@.str24 = private unnamed_addr constant [8 x i8] c"div.err\00", align 1
@.str3 = private unnamed_addr constant [8 x i8] c"IGNORED\00", align 1
@.str14 = private unnamed_addr constant [16 x i8] c"overshift error\00", align 1
@.str25 = private unnamed_addr constant [14 x i8] c"overshift.err\00", align 1
@.str6 = private unnamed_addr constant [58 x i8] c"/home/walker/Projects/klee/runtime/Intrinsic/klee_range.c\00", align 1
@.str17 = private unnamed_addr constant [14 x i8] c"invalid range\00", align 1
@.str28 = private unnamed_addr constant [5 x i8] c"user\00", align 1

define internal void @__cxx_global_var_init() section ".text.startup" {
entry:
  call void @_ZNSt8ios_base4InitC1Ev(%"class.std::ios_base::Init"* @_ZStL8__ioinit), !dbg !283
  %0 = call i32 @__cxa_atexit(void (i8*)* bitcast (void (%"class.std::ios_base::Init"*)* @_ZNSt8ios_base4InitD1Ev to void (i8*)*), i8* getelementptr inbounds (%"class.std::ios_base::Init"* @_ZStL8__ioinit, i32 0, i32 0), i8* @__dso_handle) #2, !dbg !283
  ret void, !dbg !283
}

declare void @_ZNSt8ios_base4InitC1Ev(%"class.std::ios_base::Init"*) #0

; Function Attrs: nounwind
declare void @_ZNSt8ios_base4InitD1Ev(%"class.std::ios_base::Init"*) #1

; Function Attrs: nounwind
declare i32 @__cxa_atexit(void (i8*)*, i8*, i8*) #2

; Function Attrs: nounwind uwtable
define i32 @_Z4sqrti(i32 %i) #3 {
entry:
  %i.addr = alloca i32, align 4
  store i32 %i, i32* %i.addr, align 4
  %0 = load i32* %i.addr, align 4, !dbg !284
  ret i32 %0, !dbg !284
}

; Function Attrs: nounwind readnone
declare void @llvm.dbg.declare(metadata, metadata) #4

; Function Attrs: nounwind uwtable
define i32 @_Z8evaluateRKi(i32* %x) #3 {
entry:
  %x.addr = alloca i32*, align 8
  %r = alloca i32, align 4
  %i = alloca i32, align 4
  store i32* %x, i32** %x.addr, align 8
  %0 = load i32** %x.addr, align 8, !dbg !286
  %1 = load i32* %0, align 4, !dbg !286
  store i32 %1, i32* %r, align 4, !dbg !286
  store i32 1, i32* %i, align 4, !dbg !287
  br label %for.cond, !dbg !287

for.cond:                                         ; preds = %for.body, %entry
  %2 = load i32* %i, align 4, !dbg !287
  %cmp = icmp slt i32 %2, 100000, !dbg !287
  %3 = load i32* %r, align 4, !dbg !287
  br i1 %cmp, label %for.body, label %for.end, !dbg !287

for.body:                                         ; preds = %for.cond
  %4 = load i32* %i, align 4, !dbg !287
  %call = call i32 @_Z4sqrti(i32 %4), !dbg !287
  %int_cast_to_i64 = zext i32 %call to i64
  call void @klee_div_zero_check(i64 %int_cast_to_i64), !dbg !287
  %div = sdiv i32 1, %call, !dbg !287
  %add = add nsw i32 %3, %div, !dbg !287
  store i32 %add, i32* %r, align 4, !dbg !287
  %5 = load i32* %i, align 4, !dbg !287
  %inc = add nsw i32 %5, 1, !dbg !287
  store i32 %inc, i32* %i, align 4, !dbg !287
  br label %for.cond, !dbg !287

for.end:                                          ; preds = %for.cond
  ret i32 %3, !dbg !289
}

; Function Attrs: uwtable
define i32 @main() #5 {
entry:
  call void @klee.ctor_stub()
  %x = alloca i32, align 4
  %res = alloca i32, align 4
  %agg.tmp = alloca %"struct.std::_Setprecision", align 4
  store i32 0, i32* %x, align 4, !dbg !290
  %0 = bitcast i32* %x to i8*, !dbg !291
  call void @klee_make_symbolic(i8* %0, i64 4, i8* getelementptr inbounds ([2 x i8]* @.str, i32 0, i32 0)), !dbg !291
  %call = call i32 @_Z8evaluateRKi(i32* %x), !dbg !292
  store i32 %call, i32* %res, align 4, !dbg !292
  %1 = load i32* %res, align 4, !dbg !293
  %call1 = call i32 @_Z11klee_outputIiET_PKcS0_(i8* getelementptr inbounds ([4 x i8]* @.str1, i32 0, i32 0), i32 %1), !dbg !293
  %call2 = call %"class.std::basic_ostream"* @_ZNSolsEPFRSt8ios_baseS0_E(%"class.std::basic_ostream"* @_ZSt4cout, %"class.std::ios_base"* (%"class.std::ios_base"*)* @_ZSt10scientificRSt8ios_base), !dbg !294
  %call3 = call i32 @_ZSt12setprecisioni(i32 9), !dbg !295
  %coerce.dive = getelementptr %"struct.std::_Setprecision"* %agg.tmp, i32 0, i32 0, !dbg !295
  store i32 %call3, i32* %coerce.dive, !dbg !295
  %coerce.dive4 = getelementptr %"struct.std::_Setprecision"* %agg.tmp, i32 0, i32 0, !dbg !296
  %2 = load i32* %coerce.dive4, !dbg !296
  %call5 = call %"class.std::basic_ostream"* @_ZStlsIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_St13_Setprecision(%"class.std::basic_ostream"* %call2, i32 %2), !dbg !296
  %3 = load i32* %res, align 4, !dbg !296
  %call6 = call %"class.std::basic_ostream"* @_ZNSolsEi(%"class.std::basic_ostream"* %call5, i32 %3), !dbg !296
  %call7 = call %"class.std::basic_ostream"* @_ZNSolsEPFRSoS_E(%"class.std::basic_ostream"* %call6, %"class.std::basic_ostream"* (%"class.std::basic_ostream"*)* @_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_), !dbg !296
  ret i32 0, !dbg !297
}

declare void @klee_make_symbolic(i8*, i64, i8*) #0

; Function Attrs: nounwind uwtable
define linkonce_odr i32 @_Z11klee_outputIiET_PKcS0_(i8* %name, i32 %v) #3 {
entry:
  %name.addr = alloca i8*, align 8
  %v.addr = alloca i32, align 4
  store i8* %name, i8** %name.addr, align 8
  store i32 %v, i32* %v.addr, align 4
  %0 = load i32* %v.addr, align 4, !dbg !298
  ret i32 %0, !dbg !298
}

declare %"class.std::basic_ostream"* @_ZStlsIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_St13_Setprecision(%"class.std::basic_ostream"*, i32) #0

declare %"class.std::basic_ostream"* @_ZNSolsEPFRSt8ios_baseS0_E(%"class.std::basic_ostream"*, %"class.std::ios_base"* (%"class.std::ios_base"*)*) #0

; Function Attrs: inlinehint uwtable
define linkonce_odr %"class.std::ios_base"* @_ZSt10scientificRSt8ios_base(%"class.std::ios_base"* %__base) #6 {
entry:
  %__base.addr = alloca %"class.std::ios_base"*, align 8
  store %"class.std::ios_base"* %__base, %"class.std::ios_base"** %__base.addr, align 8
  %0 = load %"class.std::ios_base"** %__base.addr, align 8, !dbg !300
  %call = call i32 @_ZNSt8ios_base4setfESt13_Ios_FmtflagsS0_(%"class.std::ios_base"* %0, i32 256, i32 260), !dbg !300
  %1 = load %"class.std::ios_base"** %__base.addr, align 8, !dbg !302
  ret %"class.std::ios_base"* %1, !dbg !302
}

; Function Attrs: inlinehint nounwind uwtable
define linkonce_odr i32 @_ZSt12setprecisioni(i32 %__n) #7 {
entry:
  %retval = alloca %"struct.std::_Setprecision", align 4
  %__n.addr = alloca i32, align 4
  store i32 %__n, i32* %__n.addr, align 4
  %_M_n = getelementptr inbounds %"struct.std::_Setprecision"* %retval, i32 0, i32 0, !dbg !303
  %0 = load i32* %__n.addr, align 4, !dbg !303
  store i32 %0, i32* %_M_n, align 4, !dbg !303
  %coerce.dive = getelementptr %"struct.std::_Setprecision"* %retval, i32 0, i32 0, !dbg !303
  %1 = load i32* %coerce.dive, !dbg !303
  ret i32 %1, !dbg !303
}

declare %"class.std::basic_ostream"* @_ZNSolsEi(%"class.std::basic_ostream"*, i32) #0

declare %"class.std::basic_ostream"* @_ZNSolsEPFRSoS_E(%"class.std::basic_ostream"*, %"class.std::basic_ostream"* (%"class.std::basic_ostream"*)*) #0

declare %"class.std::basic_ostream"* @_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_(%"class.std::basic_ostream"*) #0

; Function Attrs: uwtable
define linkonce_odr i32 @_ZNSt8ios_base4setfESt13_Ios_FmtflagsS0_(%"class.std::ios_base"* %this, i32 %__fmtfl, i32 %__mask) #5 align 2 {
entry:
  %this.addr = alloca %"class.std::ios_base"*, align 8
  %__fmtfl.addr = alloca i32, align 4
  %__mask.addr = alloca i32, align 4
  %__old = alloca i32, align 4
  store %"class.std::ios_base"* %this, %"class.std::ios_base"** %this.addr, align 8
  store i32 %__fmtfl, i32* %__fmtfl.addr, align 4
  store i32 %__mask, i32* %__mask.addr, align 4
  %this1 = load %"class.std::ios_base"** %this.addr
  %_M_flags = getelementptr inbounds %"class.std::ios_base"* %this1, i32 0, i32 3, !dbg !305
  %0 = load i32* %_M_flags, align 4, !dbg !305
  store i32 %0, i32* %__old, align 4, !dbg !305
  %_M_flags2 = getelementptr inbounds %"class.std::ios_base"* %this1, i32 0, i32 3, !dbg !306
  %1 = load i32* %__mask.addr, align 4, !dbg !307
  %call = call i32 @_ZStcoSt13_Ios_Fmtflags(i32 %1), !dbg !307
  %call3 = call i32* @_ZStaNRSt13_Ios_FmtflagsS_(i32* %_M_flags2, i32 %call), !dbg !308
  %_M_flags4 = getelementptr inbounds %"class.std::ios_base"* %this1, i32 0, i32 3, !dbg !309
  %2 = load i32* %__fmtfl.addr, align 4, !dbg !310
  %3 = load i32* %__mask.addr, align 4, !dbg !310
  %call5 = call i32 @_ZStanSt13_Ios_FmtflagsS_(i32 %2, i32 %3), !dbg !310
  %call6 = call i32* @_ZStoRRSt13_Ios_FmtflagsS_(i32* %_M_flags4, i32 %call5), !dbg !311
  %4 = load i32* %__old, align 4, !dbg !312
  ret i32 %4, !dbg !312
}

; Function Attrs: inlinehint nounwind uwtable
define linkonce_odr i32* @_ZStaNRSt13_Ios_FmtflagsS_(i32* %__a, i32 %__b) #7 {
entry:
  %__a.addr = alloca i32*, align 8
  %__b.addr = alloca i32, align 4
  store i32* %__a, i32** %__a.addr, align 8
  store i32 %__b, i32* %__b.addr, align 4
  %0 = load i32** %__a.addr, align 8, !dbg !313
  %1 = load i32* %0, align 4, !dbg !313
  %2 = load i32* %__b.addr, align 4, !dbg !313
  %call = call i32 @_ZStanSt13_Ios_FmtflagsS_(i32 %1, i32 %2), !dbg !313
  %3 = load i32** %__a.addr, align 8, !dbg !313
  store i32 %call, i32* %3, align 4, !dbg !313
  ret i32* %3, !dbg !313
}

; Function Attrs: inlinehint nounwind uwtable
define linkonce_odr i32 @_ZStcoSt13_Ios_Fmtflags(i32 %__a) #7 {
entry:
  %__a.addr = alloca i32, align 4
  store i32 %__a, i32* %__a.addr, align 4
  %0 = load i32* %__a.addr, align 4, !dbg !314
  %neg = xor i32 %0, -1, !dbg !314
  ret i32 %neg, !dbg !314
}

; Function Attrs: inlinehint uwtable
define linkonce_odr i32* @_ZStoRRSt13_Ios_FmtflagsS_(i32* %__a, i32 %__b) #6 {
entry:
  %__a.addr = alloca i32*, align 8
  %__b.addr = alloca i32, align 4
  store i32* %__a, i32** %__a.addr, align 8
  store i32 %__b, i32* %__b.addr, align 4
  %0 = load i32** %__a.addr, align 8, !dbg !315
  %1 = load i32* %0, align 4, !dbg !315
  %2 = load i32* %__b.addr, align 4, !dbg !315
  %call = call i32 @_ZStorSt13_Ios_FmtflagsS_(i32 %1, i32 %2), !dbg !315
  %3 = load i32** %__a.addr, align 8, !dbg !315
  store i32 %call, i32* %3, align 4, !dbg !315
  ret i32* %3, !dbg !315
}

; Function Attrs: inlinehint nounwind uwtable
define linkonce_odr i32 @_ZStanSt13_Ios_FmtflagsS_(i32 %__a, i32 %__b) #7 {
entry:
  %__a.addr = alloca i32, align 4
  %__b.addr = alloca i32, align 4
  store i32 %__a, i32* %__a.addr, align 4
  store i32 %__b, i32* %__b.addr, align 4
  %0 = load i32* %__a.addr, align 4, !dbg !316
  %1 = load i32* %__b.addr, align 4, !dbg !316
  %and = and i32 %0, %1, !dbg !316
  ret i32 %and, !dbg !316
}

; Function Attrs: inlinehint nounwind uwtable
define linkonce_odr i32 @_ZStorSt13_Ios_FmtflagsS_(i32 %__a, i32 %__b) #7 {
entry:
  %__a.addr = alloca i32, align 4
  %__b.addr = alloca i32, align 4
  store i32 %__a, i32* %__a.addr, align 4
  store i32 %__b, i32* %__b.addr, align 4
  %0 = load i32* %__a.addr, align 4, !dbg !317
  %1 = load i32* %__b.addr, align 4, !dbg !317
  %or = or i32 %0, %1, !dbg !317
  ret i32 %or, !dbg !317
}

define internal void @_GLOBAL__I_a() section ".text.startup" {
entry:
  call void @__cxx_global_var_init(), !dbg !318
  ret void, !dbg !318
}

; Function Attrs: nounwind uwtable
define void @klee_div_zero_check(i64 %z) #8 {
entry:
  %cmp = icmp eq i64 %z, 0, !dbg !319
  br i1 %cmp, label %if.then, label %if.end, !dbg !319

if.then:                                          ; preds = %entry
  tail call void @klee_report_error(i8* getelementptr inbounds ([67 x i8]* @.str2, i64 0, i64 0), i32 14, i8* getelementptr inbounds ([15 x i8]* @.str13, i64 0, i64 0), i8* getelementptr inbounds ([8 x i8]* @.str24, i64 0, i64 0)) #11, !dbg !321
  unreachable, !dbg !321

if.end:                                           ; preds = %entry
  ret void, !dbg !322
}

; Function Attrs: noreturn
declare void @klee_report_error(i8*, i32, i8*, i8*) #9

; Function Attrs: nounwind readnone
declare void @llvm.dbg.value(metadata, i64, metadata) #4

; Function Attrs: nounwind uwtable
define i32 @klee_int(i8* %name) #8 {
entry:
  %x = alloca i32, align 4
  %0 = bitcast i32* %x to i8*, !dbg !323
  call void @klee_make_symbolic(i8* %0, i64 4, i8* %name) #12, !dbg !323
  %1 = load i32* %x, align 4, !dbg !324, !tbaa !325
  ret i32 %1, !dbg !324
}

; Function Attrs: nounwind uwtable
define void @klee_overshift_check(i64 %bitWidth, i64 %shift) #8 {
entry:
  %cmp = icmp ult i64 %shift, %bitWidth, !dbg !329
  br i1 %cmp, label %if.end, label %if.then, !dbg !329

if.then:                                          ; preds = %entry
  tail call void @klee_report_error(i8* getelementptr inbounds ([8 x i8]* @.str3, i64 0, i64 0), i32 0, i8* getelementptr inbounds ([16 x i8]* @.str14, i64 0, i64 0), i8* getelementptr inbounds ([14 x i8]* @.str25, i64 0, i64 0)) #11, !dbg !331
  unreachable, !dbg !331

if.end:                                           ; preds = %entry
  ret void, !dbg !333
}

; Function Attrs: nounwind uwtable
define i32 @klee_range(i32 %start, i32 %end, i8* %name) #8 {
entry:
  %x = alloca i32, align 4
  %cmp = icmp slt i32 %start, %end, !dbg !334
  br i1 %cmp, label %if.end, label %if.then, !dbg !334

if.then:                                          ; preds = %entry
  call void @klee_report_error(i8* getelementptr inbounds ([58 x i8]* @.str6, i64 0, i64 0), i32 17, i8* getelementptr inbounds ([14 x i8]* @.str17, i64 0, i64 0), i8* getelementptr inbounds ([5 x i8]* @.str28, i64 0, i64 0)) #11, !dbg !336
  unreachable, !dbg !336

if.end:                                           ; preds = %entry
  %add = add nsw i32 %start, 1, !dbg !337
  %cmp1 = icmp eq i32 %add, %end, !dbg !337
  br i1 %cmp1, label %return, label %if.else, !dbg !337

if.else:                                          ; preds = %if.end
  %0 = bitcast i32* %x to i8*, !dbg !339
  call void @klee_make_symbolic(i8* %0, i64 4, i8* %name) #12, !dbg !339
  %cmp3 = icmp eq i32 %start, 0, !dbg !341
  %1 = load i32* %x, align 4, !dbg !343, !tbaa !325
  br i1 %cmp3, label %if.then4, label %if.else7, !dbg !341

if.then4:                                         ; preds = %if.else
  %cmp5 = icmp ult i32 %1, %end, !dbg !343
  %conv6 = zext i1 %cmp5 to i64, !dbg !343
  call void @klee_assume(i64 %conv6) #12, !dbg !343
  br label %if.end14, !dbg !345

if.else7:                                         ; preds = %if.else
  %cmp8 = icmp sge i32 %1, %start, !dbg !346
  %conv10 = zext i1 %cmp8 to i64, !dbg !346
  call void @klee_assume(i64 %conv10) #12, !dbg !346
  %2 = load i32* %x, align 4, !dbg !348, !tbaa !325
  %cmp11 = icmp slt i32 %2, %end, !dbg !348
  %conv13 = zext i1 %cmp11 to i64, !dbg !348
  call void @klee_assume(i64 %conv13) #12, !dbg !348
  br label %if.end14

if.end14:                                         ; preds = %if.else7, %if.then4
  %3 = load i32* %x, align 4, !dbg !349, !tbaa !325
  br label %return, !dbg !349

return:                                           ; preds = %if.end14, %if.end
  %retval.0 = phi i32 [ %3, %if.end14 ], [ %start, %if.end ]
  ret i32 %retval.0, !dbg !350
}

declare void @klee_assume(i64) #10

; Function Attrs: nounwind uwtable
define weak i8* @memcpy(i8* %destaddr, i8* %srcaddr, i64 %len) #8 {
entry:
  %cmp3 = icmp eq i64 %len, 0, !dbg !351
  br i1 %cmp3, label %while.end, label %while.body.preheader, !dbg !351

while.body.preheader:                             ; preds = %entry
  %n.vec = and i64 %len, -32
  %cmp.zero = icmp eq i64 %n.vec, 0
  %0 = add i64 %len, -1
  br i1 %cmp.zero, label %middle.block, label %vector.memcheck

vector.memcheck:                                  ; preds = %while.body.preheader
  %scevgep7 = getelementptr i8* %srcaddr, i64 %0
  %scevgep = getelementptr i8* %destaddr, i64 %0
  %bound1 = icmp uge i8* %scevgep, %srcaddr
  %bound0 = icmp uge i8* %scevgep7, %destaddr
  %memcheck.conflict = and i1 %bound0, %bound1
  %ptr.ind.end = getelementptr i8* %srcaddr, i64 %n.vec
  %ptr.ind.end9 = getelementptr i8* %destaddr, i64 %n.vec
  %rev.ind.end = sub i64 %len, %n.vec
  br i1 %memcheck.conflict, label %middle.block, label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.memcheck
  %index = phi i64 [ %index.next, %vector.body ], [ 0, %vector.memcheck ]
  %next.gep = getelementptr i8* %srcaddr, i64 %index
  %next.gep106 = getelementptr i8* %destaddr, i64 %index
  %1 = bitcast i8* %next.gep to <16 x i8>*, !dbg !352
  %wide.load = load <16 x i8>* %1, align 1, !dbg !352
  %next.gep.sum282 = or i64 %index, 16, !dbg !352
  %2 = getelementptr i8* %srcaddr, i64 %next.gep.sum282, !dbg !352
  %3 = bitcast i8* %2 to <16 x i8>*, !dbg !352
  %wide.load203 = load <16 x i8>* %3, align 1, !dbg !352
  %4 = bitcast i8* %next.gep106 to <16 x i8>*, !dbg !352
  store <16 x i8> %wide.load, <16 x i8>* %4, align 1, !dbg !352
  %5 = getelementptr i8* %destaddr, i64 %next.gep.sum282, !dbg !352
  %6 = bitcast i8* %5 to <16 x i8>*, !dbg !352
  store <16 x i8> %wide.load203, <16 x i8>* %6, align 1, !dbg !352
  %index.next = add i64 %index, 32
  %7 = icmp eq i64 %index.next, %n.vec
  br i1 %7, label %middle.block, label %vector.body, !llvm.loop !353

middle.block:                                     ; preds = %vector.body, %vector.memcheck, %while.body.preheader
  %resume.val = phi i8* [ %srcaddr, %while.body.preheader ], [ %srcaddr, %vector.memcheck ], [ %ptr.ind.end, %vector.body ]
  %resume.val8 = phi i8* [ %destaddr, %while.body.preheader ], [ %destaddr, %vector.memcheck ], [ %ptr.ind.end9, %vector.body ]
  %resume.val10 = phi i64 [ %len, %while.body.preheader ], [ %len, %vector.memcheck ], [ %rev.ind.end, %vector.body ]
  %new.indc.resume.val = phi i64 [ 0, %while.body.preheader ], [ 0, %vector.memcheck ], [ %n.vec, %vector.body ]
  %cmp.n = icmp eq i64 %new.indc.resume.val, %len
  br i1 %cmp.n, label %while.end, label %while.body

while.body:                                       ; preds = %while.body, %middle.block
  %src.06 = phi i8* [ %incdec.ptr, %while.body ], [ %resume.val, %middle.block ]
  %dest.05 = phi i8* [ %incdec.ptr1, %while.body ], [ %resume.val8, %middle.block ]
  %len.addr.04 = phi i64 [ %dec, %while.body ], [ %resume.val10, %middle.block ]
  %dec = add i64 %len.addr.04, -1, !dbg !351
  %incdec.ptr = getelementptr inbounds i8* %src.06, i64 1, !dbg !352
  %8 = load i8* %src.06, align 1, !dbg !352, !tbaa !356
  %incdec.ptr1 = getelementptr inbounds i8* %dest.05, i64 1, !dbg !352
  store i8 %8, i8* %dest.05, align 1, !dbg !352, !tbaa !356
  %cmp = icmp eq i64 %dec, 0, !dbg !351
  br i1 %cmp, label %while.end, label %while.body, !dbg !351, !llvm.loop !357

while.end:                                        ; preds = %while.body, %middle.block, %entry
  ret i8* %destaddr, !dbg !358
}

; Function Attrs: nounwind uwtable
define weak i8* @memmove(i8* %dst, i8* %src, i64 %count) #8 {
entry:
  %cmp = icmp eq i8* %src, %dst, !dbg !359
  br i1 %cmp, label %return, label %if.end, !dbg !359

if.end:                                           ; preds = %entry
  %cmp1 = icmp ugt i8* %src, %dst, !dbg !361
  br i1 %cmp1, label %while.cond.preheader, label %if.else, !dbg !361

while.cond.preheader:                             ; preds = %if.end
  %tobool27 = icmp eq i64 %count, 0, !dbg !363
  br i1 %tobool27, label %return, label %while.body.preheader, !dbg !363

while.body.preheader:                             ; preds = %while.cond.preheader
  %n.vec = and i64 %count, -32
  %cmp.zero = icmp eq i64 %n.vec, 0
  %0 = add i64 %count, -1
  br i1 %cmp.zero, label %middle.block, label %vector.memcheck

vector.memcheck:                                  ; preds = %while.body.preheader
  %scevgep37 = getelementptr i8* %src, i64 %0
  %scevgep = getelementptr i8* %dst, i64 %0
  %bound1 = icmp uge i8* %scevgep, %src
  %bound0 = icmp uge i8* %scevgep37, %dst
  %memcheck.conflict = and i1 %bound0, %bound1
  %ptr.ind.end = getelementptr i8* %src, i64 %n.vec
  %ptr.ind.end39 = getelementptr i8* %dst, i64 %n.vec
  %rev.ind.end = sub i64 %count, %n.vec
  br i1 %memcheck.conflict, label %middle.block, label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.memcheck
  %index = phi i64 [ %index.next, %vector.body ], [ 0, %vector.memcheck ]
  %next.gep = getelementptr i8* %src, i64 %index
  %next.gep136 = getelementptr i8* %dst, i64 %index
  %1 = bitcast i8* %next.gep to <16 x i8>*, !dbg !363
  %wide.load = load <16 x i8>* %1, align 1, !dbg !363
  %next.gep.sum610 = or i64 %index, 16, !dbg !363
  %2 = getelementptr i8* %src, i64 %next.gep.sum610, !dbg !363
  %3 = bitcast i8* %2 to <16 x i8>*, !dbg !363
  %wide.load233 = load <16 x i8>* %3, align 1, !dbg !363
  %4 = bitcast i8* %next.gep136 to <16 x i8>*, !dbg !363
  store <16 x i8> %wide.load, <16 x i8>* %4, align 1, !dbg !363
  %5 = getelementptr i8* %dst, i64 %next.gep.sum610, !dbg !363
  %6 = bitcast i8* %5 to <16 x i8>*, !dbg !363
  store <16 x i8> %wide.load233, <16 x i8>* %6, align 1, !dbg !363
  %index.next = add i64 %index, 32
  %7 = icmp eq i64 %index.next, %n.vec
  br i1 %7, label %middle.block, label %vector.body, !llvm.loop !365

middle.block:                                     ; preds = %vector.body, %vector.memcheck, %while.body.preheader
  %resume.val = phi i8* [ %src, %while.body.preheader ], [ %src, %vector.memcheck ], [ %ptr.ind.end, %vector.body ]
  %resume.val38 = phi i8* [ %dst, %while.body.preheader ], [ %dst, %vector.memcheck ], [ %ptr.ind.end39, %vector.body ]
  %resume.val40 = phi i64 [ %count, %while.body.preheader ], [ %count, %vector.memcheck ], [ %rev.ind.end, %vector.body ]
  %new.indc.resume.val = phi i64 [ 0, %while.body.preheader ], [ 0, %vector.memcheck ], [ %n.vec, %vector.body ]
  %cmp.n = icmp eq i64 %new.indc.resume.val, %count
  br i1 %cmp.n, label %return, label %while.body

while.body:                                       ; preds = %while.body, %middle.block
  %b.030 = phi i8* [ %incdec.ptr, %while.body ], [ %resume.val, %middle.block ]
  %a.029 = phi i8* [ %incdec.ptr3, %while.body ], [ %resume.val38, %middle.block ]
  %count.addr.028 = phi i64 [ %dec, %while.body ], [ %resume.val40, %middle.block ]
  %dec = add i64 %count.addr.028, -1, !dbg !363
  %incdec.ptr = getelementptr inbounds i8* %b.030, i64 1, !dbg !363
  %8 = load i8* %b.030, align 1, !dbg !363, !tbaa !356
  %incdec.ptr3 = getelementptr inbounds i8* %a.029, i64 1, !dbg !363
  store i8 %8, i8* %a.029, align 1, !dbg !363, !tbaa !356
  %tobool = icmp eq i64 %dec, 0, !dbg !363
  br i1 %tobool, label %return, label %while.body, !dbg !363, !llvm.loop !366

if.else:                                          ; preds = %if.end
  %sub = add i64 %count, -1, !dbg !367
  %tobool832 = icmp eq i64 %count, 0, !dbg !369
  br i1 %tobool832, label %return, label %while.body9.lr.ph, !dbg !369

while.body9.lr.ph:                                ; preds = %if.else
  %add.ptr5 = getelementptr inbounds i8* %src, i64 %sub, !dbg !370
  %add.ptr = getelementptr inbounds i8* %dst, i64 %sub, !dbg !367
  %n.vec241 = and i64 %count, -32
  %cmp.zero243 = icmp eq i64 %n.vec241, 0
  br i1 %cmp.zero243, label %middle.block236, label %vector.memcheck250

vector.memcheck250:                               ; preds = %while.body9.lr.ph
  %bound1247 = icmp ule i8* %add.ptr5, %dst
  %bound0246 = icmp ule i8* %add.ptr, %src
  %memcheck.conflict249 = and i1 %bound0246, %bound1247
  %add.ptr5.sum = sub i64 %sub, %n.vec241
  %rev.ptr.ind.end = getelementptr i8* %src, i64 %add.ptr5.sum
  %rev.ptr.ind.end255 = getelementptr i8* %dst, i64 %add.ptr5.sum
  %rev.ind.end257 = sub i64 %count, %n.vec241
  br i1 %memcheck.conflict249, label %middle.block236, label %vector.body235

vector.body235:                                   ; preds = %vector.body235, %vector.memcheck250
  %index238 = phi i64 [ %index.next260, %vector.body235 ], [ 0, %vector.memcheck250 ]
  %add.ptr5.sum465 = sub i64 %sub, %index238
  %next.gep262.sum = add i64 %add.ptr5.sum465, -15, !dbg !369
  %9 = getelementptr i8* %src, i64 %next.gep262.sum, !dbg !369
  %10 = bitcast i8* %9 to <16 x i8>*, !dbg !369
  %wide.load460 = load <16 x i8>* %10, align 1, !dbg !369
  %reverse = shufflevector <16 x i8> %wide.load460, <16 x i8> undef, <16 x i32> <i32 15, i32 14, i32 13, i32 12, i32 11, i32 10, i32 9, i32 8, i32 7, i32 6, i32 5, i32 4, i32 3, i32 2, i32 1, i32 0>, !dbg !369
  %.sum = add i64 %add.ptr5.sum465, -31, !dbg !369
  %11 = getelementptr i8* %src, i64 %.sum, !dbg !369
  %12 = bitcast i8* %11 to <16 x i8>*, !dbg !369
  %wide.load461 = load <16 x i8>* %12, align 1, !dbg !369
  %reverse462 = shufflevector <16 x i8> %wide.load461, <16 x i8> undef, <16 x i32> <i32 15, i32 14, i32 13, i32 12, i32 11, i32 10, i32 9, i32 8, i32 7, i32 6, i32 5, i32 4, i32 3, i32 2, i32 1, i32 0>, !dbg !369
  %reverse463 = shufflevector <16 x i8> %reverse, <16 x i8> undef, <16 x i32> <i32 15, i32 14, i32 13, i32 12, i32 11, i32 10, i32 9, i32 8, i32 7, i32 6, i32 5, i32 4, i32 3, i32 2, i32 1, i32 0>, !dbg !369
  %13 = getelementptr i8* %dst, i64 %next.gep262.sum, !dbg !369
  %14 = bitcast i8* %13 to <16 x i8>*, !dbg !369
  store <16 x i8> %reverse463, <16 x i8>* %14, align 1, !dbg !369
  %reverse464 = shufflevector <16 x i8> %reverse462, <16 x i8> undef, <16 x i32> <i32 15, i32 14, i32 13, i32 12, i32 11, i32 10, i32 9, i32 8, i32 7, i32 6, i32 5, i32 4, i32 3, i32 2, i32 1, i32 0>, !dbg !369
  %15 = getelementptr i8* %dst, i64 %.sum, !dbg !369
  %16 = bitcast i8* %15 to <16 x i8>*, !dbg !369
  store <16 x i8> %reverse464, <16 x i8>* %16, align 1, !dbg !369
  %index.next260 = add i64 %index238, 32
  %17 = icmp eq i64 %index.next260, %n.vec241
  br i1 %17, label %middle.block236, label %vector.body235, !llvm.loop !371

middle.block236:                                  ; preds = %vector.body235, %vector.memcheck250, %while.body9.lr.ph
  %resume.val251 = phi i8* [ %add.ptr5, %while.body9.lr.ph ], [ %add.ptr5, %vector.memcheck250 ], [ %rev.ptr.ind.end, %vector.body235 ]
  %resume.val253 = phi i8* [ %add.ptr, %while.body9.lr.ph ], [ %add.ptr, %vector.memcheck250 ], [ %rev.ptr.ind.end255, %vector.body235 ]
  %resume.val256 = phi i64 [ %count, %while.body9.lr.ph ], [ %count, %vector.memcheck250 ], [ %rev.ind.end257, %vector.body235 ]
  %new.indc.resume.val258 = phi i64 [ 0, %while.body9.lr.ph ], [ 0, %vector.memcheck250 ], [ %n.vec241, %vector.body235 ]
  %cmp.n259 = icmp eq i64 %new.indc.resume.val258, %count
  br i1 %cmp.n259, label %return, label %while.body9

while.body9:                                      ; preds = %while.body9, %middle.block236
  %b.135 = phi i8* [ %incdec.ptr10, %while.body9 ], [ %resume.val251, %middle.block236 ]
  %a.134 = phi i8* [ %incdec.ptr11, %while.body9 ], [ %resume.val253, %middle.block236 ]
  %count.addr.133 = phi i64 [ %dec7, %while.body9 ], [ %resume.val256, %middle.block236 ]
  %dec7 = add i64 %count.addr.133, -1, !dbg !369
  %incdec.ptr10 = getelementptr inbounds i8* %b.135, i64 -1, !dbg !369
  %18 = load i8* %b.135, align 1, !dbg !369, !tbaa !356
  %incdec.ptr11 = getelementptr inbounds i8* %a.134, i64 -1, !dbg !369
  store i8 %18, i8* %a.134, align 1, !dbg !369, !tbaa !356
  %tobool8 = icmp eq i64 %dec7, 0, !dbg !369
  br i1 %tobool8, label %return, label %while.body9, !dbg !369, !llvm.loop !372

return:                                           ; preds = %while.body9, %middle.block236, %if.else, %while.body, %middle.block, %while.cond.preheader, %entry
  ret i8* %dst, !dbg !373
}

; Function Attrs: nounwind uwtable
define weak i8* @mempcpy(i8* %destaddr, i8* %srcaddr, i64 %len) #8 {
entry:
  %cmp3 = icmp eq i64 %len, 0, !dbg !374
  br i1 %cmp3, label %while.end, label %while.body.preheader, !dbg !374

while.body.preheader:                             ; preds = %entry
  %n.vec = and i64 %len, -32
  %cmp.zero = icmp eq i64 %n.vec, 0
  %0 = add i64 %len, -1
  br i1 %cmp.zero, label %middle.block, label %vector.memcheck

vector.memcheck:                                  ; preds = %while.body.preheader
  %scevgep8 = getelementptr i8* %srcaddr, i64 %0
  %scevgep7 = getelementptr i8* %destaddr, i64 %0
  %bound1 = icmp uge i8* %scevgep7, %srcaddr
  %bound0 = icmp uge i8* %scevgep8, %destaddr
  %memcheck.conflict = and i1 %bound0, %bound1
  %ptr.ind.end = getelementptr i8* %srcaddr, i64 %n.vec
  %ptr.ind.end10 = getelementptr i8* %destaddr, i64 %n.vec
  %rev.ind.end = sub i64 %len, %n.vec
  br i1 %memcheck.conflict, label %middle.block, label %vector.body

vector.body:                                      ; preds = %vector.body, %vector.memcheck
  %index = phi i64 [ %index.next, %vector.body ], [ 0, %vector.memcheck ]
  %next.gep = getelementptr i8* %srcaddr, i64 %index
  %next.gep107 = getelementptr i8* %destaddr, i64 %index
  %1 = bitcast i8* %next.gep to <16 x i8>*, !dbg !375
  %wide.load = load <16 x i8>* %1, align 1, !dbg !375
  %next.gep.sum283 = or i64 %index, 16, !dbg !375
  %2 = getelementptr i8* %srcaddr, i64 %next.gep.sum283, !dbg !375
  %3 = bitcast i8* %2 to <16 x i8>*, !dbg !375
  %wide.load204 = load <16 x i8>* %3, align 1, !dbg !375
  %4 = bitcast i8* %next.gep107 to <16 x i8>*, !dbg !375
  store <16 x i8> %wide.load, <16 x i8>* %4, align 1, !dbg !375
  %5 = getelementptr i8* %destaddr, i64 %next.gep.sum283, !dbg !375
  %6 = bitcast i8* %5 to <16 x i8>*, !dbg !375
  store <16 x i8> %wide.load204, <16 x i8>* %6, align 1, !dbg !375
  %index.next = add i64 %index, 32
  %7 = icmp eq i64 %index.next, %n.vec
  br i1 %7, label %middle.block, label %vector.body, !llvm.loop !376

middle.block:                                     ; preds = %vector.body, %vector.memcheck, %while.body.preheader
  %resume.val = phi i8* [ %srcaddr, %while.body.preheader ], [ %srcaddr, %vector.memcheck ], [ %ptr.ind.end, %vector.body ]
  %resume.val9 = phi i8* [ %destaddr, %while.body.preheader ], [ %destaddr, %vector.memcheck ], [ %ptr.ind.end10, %vector.body ]
  %resume.val11 = phi i64 [ %len, %while.body.preheader ], [ %len, %vector.memcheck ], [ %rev.ind.end, %vector.body ]
  %new.indc.resume.val = phi i64 [ 0, %while.body.preheader ], [ 0, %vector.memcheck ], [ %n.vec, %vector.body ]
  %cmp.n = icmp eq i64 %new.indc.resume.val, %len
  br i1 %cmp.n, label %while.cond.while.end_crit_edge, label %while.body

while.body:                                       ; preds = %while.body, %middle.block
  %src.06 = phi i8* [ %incdec.ptr, %while.body ], [ %resume.val, %middle.block ]
  %dest.05 = phi i8* [ %incdec.ptr1, %while.body ], [ %resume.val9, %middle.block ]
  %len.addr.04 = phi i64 [ %dec, %while.body ], [ %resume.val11, %middle.block ]
  %dec = add i64 %len.addr.04, -1, !dbg !374
  %incdec.ptr = getelementptr inbounds i8* %src.06, i64 1, !dbg !375
  %8 = load i8* %src.06, align 1, !dbg !375, !tbaa !356
  %incdec.ptr1 = getelementptr inbounds i8* %dest.05, i64 1, !dbg !375
  store i8 %8, i8* %dest.05, align 1, !dbg !375, !tbaa !356
  %cmp = icmp eq i64 %dec, 0, !dbg !374
  br i1 %cmp, label %while.cond.while.end_crit_edge, label %while.body, !dbg !374, !llvm.loop !377

while.cond.while.end_crit_edge:                   ; preds = %while.body, %middle.block
  %scevgep = getelementptr i8* %destaddr, i64 %len
  br label %while.end, !dbg !374

while.end:                                        ; preds = %while.cond.while.end_crit_edge, %entry
  %dest.0.lcssa = phi i8* [ %scevgep, %while.cond.while.end_crit_edge ], [ %destaddr, %entry ]
  ret i8* %dest.0.lcssa, !dbg !378
}

; Function Attrs: nounwind uwtable
define weak i8* @memset(i8* %dst, i32 %s, i64 %count) #8 {
entry:
  %cmp2 = icmp eq i64 %count, 0, !dbg !379
  br i1 %cmp2, label %while.end, label %while.body.lr.ph, !dbg !379

while.body.lr.ph:                                 ; preds = %entry
  %conv = trunc i32 %s to i8, !dbg !380
  br label %while.body, !dbg !379

while.body:                                       ; preds = %while.body, %while.body.lr.ph
  %a.04 = phi i8* [ %dst, %while.body.lr.ph ], [ %incdec.ptr, %while.body ]
  %count.addr.03 = phi i64 [ %count, %while.body.lr.ph ], [ %dec, %while.body ]
  %dec = add i64 %count.addr.03, -1, !dbg !379
  %incdec.ptr = getelementptr inbounds i8* %a.04, i64 1, !dbg !380
  store volatile i8 %conv, i8* %a.04, align 1, !dbg !380, !tbaa !356
  %cmp = icmp eq i64 %dec, 0, !dbg !379
  br i1 %cmp, label %while.end, label %while.body, !dbg !379

while.end:                                        ; preds = %while.body, %entry
  ret i8* %dst, !dbg !381
}

define internal void @klee.ctor_stub() {
entry:
  call void @_GLOBAL__I_a()
  ret void
}

attributes #0 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false
attributes #2 = { nounwind }
attributes #3 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float
attributes #4 = { nounwind readnone }
attributes #5 = { uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false"
attributes #6 = { inlinehint uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-flo
attributes #7 = { inlinehint nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use
attributes #8 = { nounwind uwtable "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #9 = { noreturn "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #10 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #11 = { nobuiltin noreturn nounwind }
attributes #12 = { nobuiltin nounwind }

!llvm.dbg.cu = !{!0, !175, !185, !195, !206, !218, !237, !251, !265}
!llvm.module.flags = !{!280, !281}
!llvm.ident = !{!282, !282, !282, !282, !282, !282, !282, !282, !282}

!0 = metadata !{i32 786449, metadata !1, i32 4, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 false, metadata !"", i32 0, metadata !2, metadata !42, metadata !112, metadata !162, metadata !169, metadata !""} ; [ DW_TAG_compile_unit ] [/home/w
!1 = metadata !{metadata !"float_extension_i.cc", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!2 = metadata !{metadata !3, metadata !11, metadata !18}
!3 = metadata !{i32 786436, metadata !4, metadata !5, metadata !"float_denorm_style", i32 182, i64 32, i64 32, i32 0, i32 0, null, metadata !7, i32 0, null, null, metadata !"_ZTSSt18float_denorm_style"} ; [ DW_TAG_enumeration_type ] [float_denorm_style] 
!4 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/limits", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!5 = metadata !{i32 786489, metadata !6, null, metadata !"std", i32 194} ; [ DW_TAG_namespace ] [std] [line 194]
!6 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/x86_64-linux-gnu/c++/5.4.0/bits/c++config.h", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!7 = metadata !{metadata !8, metadata !9, metadata !10}
!8 = metadata !{i32 786472, metadata !"denorm_indeterminate", i64 -1} ; [ DW_TAG_enumerator ] [denorm_indeterminate :: -1]
!9 = metadata !{i32 786472, metadata !"denorm_absent", i64 0} ; [ DW_TAG_enumerator ] [denorm_absent :: 0]
!10 = metadata !{i32 786472, metadata !"denorm_present", i64 1} ; [ DW_TAG_enumerator ] [denorm_present :: 1]
!11 = metadata !{i32 786436, metadata !4, metadata !5, metadata !"float_round_style", i32 167, i64 32, i64 32, i32 0, i32 0, null, metadata !12, i32 0, null, null, metadata !"_ZTSSt17float_round_style"} ; [ DW_TAG_enumeration_type ] [float_round_style] [
!12 = metadata !{metadata !13, metadata !14, metadata !15, metadata !16, metadata !17}
!13 = metadata !{i32 786472, metadata !"round_indeterminate", i64 -1} ; [ DW_TAG_enumerator ] [round_indeterminate :: -1]
!14 = metadata !{i32 786472, metadata !"round_toward_zero", i64 0} ; [ DW_TAG_enumerator ] [round_toward_zero :: 0]
!15 = metadata !{i32 786472, metadata !"round_to_nearest", i64 1} ; [ DW_TAG_enumerator ] [round_to_nearest :: 1]
!16 = metadata !{i32 786472, metadata !"round_toward_infinity", i64 2} ; [ DW_TAG_enumerator ] [round_toward_infinity :: 2]
!17 = metadata !{i32 786472, metadata !"round_toward_neg_infinity", i64 3} ; [ DW_TAG_enumerator ] [round_toward_neg_infinity :: 3]
!18 = metadata !{i32 786436, metadata !19, metadata !5, metadata !"_Ios_Fmtflags", i32 57, i64 32, i64 32, i32 0, i32 0, null, metadata !20, i32 0, null, null, metadata !"_ZTSSt13_Ios_Fmtflags"} ; [ DW_TAG_enumeration_type ] [_Ios_Fmtflags] [line 57, siz
!19 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/ios_base.h", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!20 = metadata !{metadata !21, metadata !22, metadata !23, metadata !24, metadata !25, metadata !26, metadata !27, metadata !28, metadata !29, metadata !30, metadata !31, metadata !32, metadata !33, metadata !34, metadata !35, metadata !36, metadata !37,
!21 = metadata !{i32 786472, metadata !"_S_boolalpha", i64 1} ; [ DW_TAG_enumerator ] [_S_boolalpha :: 1]
!22 = metadata !{i32 786472, metadata !"_S_dec", i64 2} ; [ DW_TAG_enumerator ] [_S_dec :: 2]
!23 = metadata !{i32 786472, metadata !"_S_fixed", i64 4} ; [ DW_TAG_enumerator ] [_S_fixed :: 4]
!24 = metadata !{i32 786472, metadata !"_S_hex", i64 8} ; [ DW_TAG_enumerator ] [_S_hex :: 8]
!25 = metadata !{i32 786472, metadata !"_S_internal", i64 16} ; [ DW_TAG_enumerator ] [_S_internal :: 16]
!26 = metadata !{i32 786472, metadata !"_S_left", i64 32} ; [ DW_TAG_enumerator ] [_S_left :: 32]
!27 = metadata !{i32 786472, metadata !"_S_oct", i64 64} ; [ DW_TAG_enumerator ] [_S_oct :: 64]
!28 = metadata !{i32 786472, metadata !"_S_right", i64 128} ; [ DW_TAG_enumerator ] [_S_right :: 128]
!29 = metadata !{i32 786472, metadata !"_S_scientific", i64 256} ; [ DW_TAG_enumerator ] [_S_scientific :: 256]
!30 = metadata !{i32 786472, metadata !"_S_showbase", i64 512} ; [ DW_TAG_enumerator ] [_S_showbase :: 512]
!31 = metadata !{i32 786472, metadata !"_S_showpoint", i64 1024} ; [ DW_TAG_enumerator ] [_S_showpoint :: 1024]
!32 = metadata !{i32 786472, metadata !"_S_showpos", i64 2048} ; [ DW_TAG_enumerator ] [_S_showpos :: 2048]
!33 = metadata !{i32 786472, metadata !"_S_skipws", i64 4096} ; [ DW_TAG_enumerator ] [_S_skipws :: 4096]
!34 = metadata !{i32 786472, metadata !"_S_unitbuf", i64 8192} ; [ DW_TAG_enumerator ] [_S_unitbuf :: 8192]
!35 = metadata !{i32 786472, metadata !"_S_uppercase", i64 16384} ; [ DW_TAG_enumerator ] [_S_uppercase :: 16384]
!36 = metadata !{i32 786472, metadata !"_S_adjustfield", i64 176} ; [ DW_TAG_enumerator ] [_S_adjustfield :: 176]
!37 = metadata !{i32 786472, metadata !"_S_basefield", i64 74} ; [ DW_TAG_enumerator ] [_S_basefield :: 74]
!38 = metadata !{i32 786472, metadata !"_S_floatfield", i64 260} ; [ DW_TAG_enumerator ] [_S_floatfield :: 260]
!39 = metadata !{i32 786472, metadata !"_S_ios_fmtflags_end", i64 65536} ; [ DW_TAG_enumerator ] [_S_ios_fmtflags_end :: 65536]
!40 = metadata !{i32 786472, metadata !"_S_ios_fmtflags_max", i64 2147483647} ; [ DW_TAG_enumerator ] [_S_ios_fmtflags_max :: 2147483647]
!41 = metadata !{i32 786472, metadata !"_S_ios_fmtflags_min", i64 -2147483648} ; [ DW_TAG_enumerator ] [_S_ios_fmtflags_min :: -2147483648]
!42 = metadata !{metadata !43, metadata !54, metadata !66, metadata !3, metadata !11, metadata !108, metadata !18}
!43 = metadata !{i32 786434, metadata !19, metadata !5, metadata !"ios_base", i32 228, i64 0, i64 0, i32 0, i32 4, null, metadata !44, i32 0, null, null, metadata !"_ZTSSt8ios_base"} ; [ DW_TAG_class_type ] [ios_base] [line 228, size 0, align 0, offset 0
!44 = metadata !{metadata !45, metadata !48, metadata !49}
!45 = metadata !{i32 786445, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"scientific", i32 354, i64 0, i64 0, i64 0, i32 4096, metadata !46, i32 256} ; [ DW_TAG_member ] [scientific] [line 354, size 0, align 0, offset 0] [static] [from ]
!46 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !47} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from fmtflags]
!47 = metadata !{i32 786454, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"fmtflags", i32 323, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt13_Ios_Fmtflags"} ; [ DW_TAG_typedef ] [fmtflags] [line 323, size 0, align 0, offset 0] [from _ZTSSt13_Ios
!48 = metadata !{i32 786445, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"floatfield", i32 384, i64 0, i64 0, i64 0, i32 4096, metadata !46, i32 260} ; [ DW_TAG_member ] [floatfield] [line 384, size 0, align 0, offset 0] [static] [from ]
!49 = metadata !{i32 786478, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"setf", metadata !"setf", metadata !"_ZNSt8ios_base4setfESt13_Ios_FmtflagsS0_", i32 663, metadata !50, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, null, null
!50 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !51, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!51 = metadata !{metadata !47, metadata !52, metadata !47, metadata !47}
!52 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 1088, metadata !"_ZTSSt8ios_base"} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [artificial] [from _ZTSSt8ios_base]
!53 = metadata !{i32 786468}
!54 = metadata !{i32 786434, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"Init", i32 601, i64 8, i64 8, i32 0, i32 0, null, metadata !55, i32 0, null, null, metadata !"_ZTSNSt8ios_base4InitE"} ; [ DW_TAG_class_type ] [Init] [line 601, size 8, al
!55 = metadata !{metadata !56, metadata !59, metadata !61, metadata !65}
!56 = metadata !{i32 786445, metadata !19, metadata !"_ZTSNSt8ios_base4InitE", metadata !"_S_refcount", i32 609, i64 0, i64 0, i64 0, i32 4097, metadata !57, null} ; [ DW_TAG_member ] [_S_refcount] [line 609, size 0, align 0, offset 0] [private] [static]
!57 = metadata !{i32 786454, metadata !19, null, metadata !"_Atomic_word", i32 32, i64 0, i64 0, i64 0, i32 0, metadata !58} ; [ DW_TAG_typedef ] [_Atomic_word] [line 32, size 0, align 0, offset 0] [from int]
!58 = metadata !{i32 786468, null, null, metadata !"int", i32 0, i64 32, i64 32, i64 0, i32 0, i32 5} ; [ DW_TAG_base_type ] [int] [line 0, size 32, align 32, offset 0, enc DW_ATE_signed]
!59 = metadata !{i32 786445, metadata !19, metadata !"_ZTSNSt8ios_base4InitE", metadata !"_S_synced_with_stdio", i32 610, i64 0, i64 0, i64 0, i32 4097, metadata !60, null} ; [ DW_TAG_member ] [_S_synced_with_stdio] [line 610, size 0, align 0, offset 0] 
!60 = metadata !{i32 786468, null, null, metadata !"bool", i32 0, i64 8, i64 8, i64 0, i32 0, i32 2} ; [ DW_TAG_base_type ] [bool] [line 0, size 8, align 8, offset 0, enc DW_ATE_boolean]
!61 = metadata !{i32 786478, metadata !19, metadata !"_ZTSNSt8ios_base4InitE", metadata !"Init", metadata !"Init", metadata !"", i32 605, metadata !62, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, null, null, i32 0, metadata !53, i32 605} ;
!62 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !63, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!63 = metadata !{null, metadata !64}
!64 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 1088, metadata !"_ZTSNSt8ios_base4InitE"} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [artificial] [from _ZTSNSt8ios_base4InitE]
!65 = metadata !{i32 786478, metadata !19, metadata !"_ZTSNSt8ios_base4InitE", metadata !"~Init", metadata !"~Init", metadata !"", i32 606, metadata !62, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, null, null, i32 0, metadata !53, i32 606}
!66 = metadata !{i32 786451, metadata !4, metadata !5, metadata !"numeric_limits<int>", i32 993, i64 8, i64 8, i32 0, i32 0, null, metadata !67, i32 0, null, metadata !106, metadata !"_ZTSSt14numeric_limitsIiE"} ; [ DW_TAG_structure_type ] [numeric_limit
!67 = metadata !{metadata !68, metadata !70, metadata !72, metadata !73, metadata !74, metadata !75, metadata !76, metadata !77, metadata !78, metadata !79, metadata !80, metadata !81, metadata !82, metadata !83, metadata !84, metadata !85, metadata !87,
!68 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_specialized", i32 995, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [is_specialized] [line 995, size 0, align 0, offset 0] [static
!69 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !60} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from bool]
!70 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"digits", i32 1008, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 31} ; [ DW_TAG_member ] [digits] [line 1008, size 0, align 0, offset 0] [static] [from ]
!71 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !58} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from int]
!72 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"digits10", i32 1009, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 9} ; [ DW_TAG_member ] [digits10] [line 1009, size 0, align 0, offset 0] [static] [from ]
!73 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"max_digits10", i32 1011, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 0} ; [ DW_TAG_member ] [max_digits10] [line 1011, size 0, align 0, offset 0] [static] [f
!74 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_signed", i32 1013, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [is_signed] [line 1013, size 0, align 0, offset 0] [static] [from 
!75 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_integer", i32 1014, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [is_integer] [line 1014, size 0, align 0, offset 0] [static] [fro
!76 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_exact", i32 1015, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [is_exact] [line 1015, size 0, align 0, offset 0] [static] [from ]
!77 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"radix", i32 1016, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 2} ; [ DW_TAG_member ] [radix] [line 1016, size 0, align 0, offset 0] [static] [from ]
!78 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"min_exponent", i32 1024, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 0} ; [ DW_TAG_member ] [min_exponent] [line 1024, size 0, align 0, offset 0] [static] [f
!79 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"min_exponent10", i32 1025, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 0} ; [ DW_TAG_member ] [min_exponent10] [line 1025, size 0, align 0, offset 0] [static
!80 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"max_exponent", i32 1026, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 0} ; [ DW_TAG_member ] [max_exponent] [line 1026, size 0, align 0, offset 0] [static] [f
!81 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"max_exponent10", i32 1027, i64 0, i64 0, i64 0, i32 4096, metadata !71, i32 0} ; [ DW_TAG_member ] [max_exponent10] [line 1027, size 0, align 0, offset 0] [static
!82 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"has_infinity", i32 1029, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [has_infinity] [line 1029, size 0, align 0, offset 0] [static]
!83 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"has_quiet_NaN", i32 1030, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [has_quiet_NaN] [line 1030, size 0, align 0, offset 0] [stati
!84 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"has_signaling_NaN", i32 1031, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [has_signaling_NaN] [line 1031, size 0, align 0, offset 0
!85 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"has_denorm", i32 1032, i64 0, i64 0, i64 0, i32 4096, metadata !86, i32 0} ; [ DW_TAG_member ] [has_denorm] [line 1032, size 0, align 0, offset 0] [static] [from 
!86 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt18float_denorm_style"} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from _ZTSSt18float_denorm_style]
!87 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"has_denorm_loss", i32 1034, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [has_denorm_loss] [line 1034, size 0, align 0, offset 0] [s
!88 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_iec559", i32 1048, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [is_iec559] [line 1048, size 0, align 0, offset 0] [static] [from
!89 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_bounded", i32 1049, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [is_bounded] [line 1049, size 0, align 0, offset 0] [static] [fro
!90 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"is_modulo", i32 1050, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [is_modulo] [line 1050, size 0, align 0, offset 0] [static] [from
!91 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"traps", i32 1052, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 true} ; [ DW_TAG_member ] [traps] [line 1052, size 0, align 0, offset 0] [static] [from ]
!92 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"tinyness_before", i32 1053, i64 0, i64 0, i64 0, i32 4096, metadata !69, i1 false} ; [ DW_TAG_member ] [tinyness_before] [line 1053, size 0, align 0, offset 0] [s
!93 = metadata !{i32 786445, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"round_style", i32 1054, i64 0, i64 0, i64 0, i32 4096, metadata !94, i32 0} ; [ DW_TAG_member ] [round_style] [line 1054, size 0, align 0, offset 0] [static] [fro
!94 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt17float_round_style"} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from _ZTSSt17float_round_style]
!95 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"min", metadata !"min", metadata !"_ZNSt14numeric_limitsIiE3minEv", i32 998, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, null, null, i
!96 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !97, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!97 = metadata !{metadata !58}
!98 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"max", metadata !"max", metadata !"_ZNSt14numeric_limitsIiE3maxEv", i32 1001, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, null, null, 
!99 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"lowest", metadata !"lowest", metadata !"_ZNSt14numeric_limitsIiE6lowestEv", i32 1005, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false, nul
!100 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"epsilon", metadata !"epsilon", metadata !"_ZNSt14numeric_limitsIiE7epsilonEv", i32 1019, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 false,
!101 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"round_error", metadata !"round_error", metadata !"_ZNSt14numeric_limitsIiE11round_errorEv", i32 1022, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 2
!102 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"infinity", metadata !"infinity", metadata !"_ZNSt14numeric_limitsIiE8infinityEv", i32 1037, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 fal
!103 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"quiet_NaN", metadata !"quiet_NaN", metadata !"_ZNSt14numeric_limitsIiE9quiet_NaNEv", i32 1040, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256, i1 
!104 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"signaling_NaN", metadata !"signaling_NaN", metadata !"_ZNSt14numeric_limitsIiE13signaling_NaNEv", i32 1043, metadata !96, i1 false, i1 false, i32 0, i32 0, null,
!105 = metadata !{i32 786478, metadata !4, metadata !"_ZTSSt14numeric_limitsIiE", metadata !"denorm_min", metadata !"denorm_min", metadata !"_ZNSt14numeric_limitsIiE10denorm_minEv", i32 1046, metadata !96, i1 false, i1 false, i32 0, i32 0, null, i32 256,
!106 = metadata !{metadata !107}
!107 = metadata !{i32 786479, null, metadata !"_Tp", metadata !58, null, i32 0, i32 0} ; [ DW_TAG_template_type_parameter ]
!108 = metadata !{i32 786451, metadata !109, metadata !5, metadata !"_Setprecision", i32 185, i64 32, i64 32, i32 0, i32 0, null, metadata !110, i32 0, null, null, metadata !"_ZTSSt13_Setprecision"} ; [ DW_TAG_structure_type ] [_Setprecision] [line 185, 
!109 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/iomanip", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!110 = metadata !{metadata !111}
!111 = metadata !{i32 786445, metadata !109, metadata !"_ZTSSt13_Setprecision", metadata !"_M_n", i32 185, i64 32, i64 32, i64 0, i32 0, metadata !58} ; [ DW_TAG_member ] [_M_n] [line 185, size 32, align 32, offset 0] [from int]
!112 = metadata !{metadata !113, metadata !119, metadata !123, metadata !127, metadata !128, metadata !138, metadata !141, metadata !145, metadata !146, metadata !149, metadata !155, metadata !156, metadata !159, metadata !160}
!113 = metadata !{i32 786478, metadata !114, metadata !115, metadata !"__cxx_global_var_init", metadata !"__cxx_global_var_init", metadata !"", i32 74, metadata !116, i1 true, i1 true, i32 0, i32 0, null, i32 256, i1 false, void ()* @__cxx_global_var_ini
!114 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/iostream", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!115 = metadata !{i32 786473, metadata !114}      ; [ DW_TAG_file_type ] [/home/walker/Projects/Experiment/1/case/float_extension//usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/iostream]
!116 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !117, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!117 = metadata !{null}
!118 = metadata !{i32 0}
!119 = metadata !{i32 786478, metadata !1, metadata !120, metadata !"sqrt", metadata !"sqrt", metadata !"_Z4sqrti", i32 8, metadata !121, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32)* @_Z4sqrti, null, null, metadata !118, i32 8} ; 
!120 = metadata !{i32 786473, metadata !1}        ; [ DW_TAG_file_type ] [/home/walker/Projects/Experiment/1/case/float_extension/float_extension_i.cc]
!121 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !122, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!122 = metadata !{metadata !58, metadata !58}
!123 = metadata !{i32 786478, metadata !1, metadata !120, metadata !"evaluate", metadata !"evaluate", metadata !"_Z8evaluateRKi", i32 14, metadata !124, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32*)* @_Z8evaluateRKi, null, null, me
!124 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !125, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!125 = metadata !{metadata !58, metadata !126}
!126 = metadata !{i32 786448, null, null, null, i32 0, i64 0, i64 0, i64 0, i32 0, metadata !71} ; [ DW_TAG_reference_type ] [line 0, size 0, align 0, offset 0] [from ]
!127 = metadata !{i32 786478, metadata !1, metadata !120, metadata !"main", metadata !"main", metadata !"", i32 21, metadata !96, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 ()* @main, null, null, metadata !118, i32 21} ; [ DW_TAG_subpr
!128 = metadata !{i32 786478, metadata !129, metadata !130, metadata !"klee_output<int>", metadata !"klee_output<int>", metadata !"_Z11klee_outputIiET_PKcS0_", i32 2, metadata !131, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i8*, i32)
!129 = metadata !{metadata !"/home/walker/Projects/klee/include/klee/klee-expression.h", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!130 = metadata !{i32 786473, metadata !129}      ; [ DW_TAG_file_type ] [/home/walker/Projects/Experiment/1/case/float_extension//home/walker/Projects/klee/include/klee/klee-expression.h]
!131 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !132, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!132 = metadata !{metadata !58, metadata !133, metadata !58}
!133 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 0, metadata !134} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [from ]
!134 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !135} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from char]
!135 = metadata !{i32 786468, null, null, metadata !"char", i32 0, i64 8, i64 8, i64 0, i32 0, i32 6} ; [ DW_TAG_base_type ] [char] [line 0, size 8, align 8, offset 0, enc DW_ATE_signed_char]
!136 = metadata !{metadata !137}
!137 = metadata !{i32 786479, null, metadata !"T", metadata !58, null, i32 0, i32 0} ; [ DW_TAG_template_type_parameter ]
!138 = metadata !{i32 786478, metadata !109, metadata !5, metadata !"setprecision", metadata !"setprecision", metadata !"_ZSt12setprecisioni", i32 195, metadata !139, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32)* @_ZSt12setprecisio
!139 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !140, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!140 = metadata !{metadata !108, metadata !58}
!141 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"scientific", metadata !"scientific", metadata !"_ZSt10scientificRSt8ios_base", i32 1049, metadata !142, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, %"class.std::ios_base"* 
!142 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !143, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!143 = metadata !{metadata !144, metadata !144}
!144 = metadata !{i32 786448, null, null, null, i32 0, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt8ios_base"} ; [ DW_TAG_reference_type ] [line 0, size 0, align 0, offset 0] [from _ZTSSt8ios_base]
!145 = metadata !{i32 786478, metadata !19, metadata !"_ZTSSt8ios_base", metadata !"setf", metadata !"setf", metadata !"_ZNSt8ios_base4setfESt13_Ios_FmtflagsS0_", i32 663, metadata !50, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (%"cla
!146 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"operator&", metadata !"operator&", metadata !"_ZStanSt13_Ios_FmtflagsS_", i32 83, metadata !147, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32, i32)* @_ZStanSt13_Ios
!147 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !148, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!148 = metadata !{metadata !18, metadata !18, metadata !18}
!149 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"operator|=", metadata !"operator|=", metadata !"_ZStoRRSt13_Ios_FmtflagsS_", i32 99, metadata !150, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32* (i32*, i32)* @_ZStoRRSt
!150 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !151, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!151 = metadata !{metadata !152, metadata !154, metadata !18}
!152 = metadata !{i32 786448, null, null, null, i32 0, i64 0, i64 0, i64 0, i32 0, metadata !153} ; [ DW_TAG_reference_type ] [line 0, size 0, align 0, offset 0] [from ]
!153 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt13_Ios_Fmtflags"} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from _ZTSSt13_Ios_Fmtflags]
!154 = metadata !{i32 786448, null, null, null, i32 0, i64 0, i64 0, i64 0, i32 0, metadata !"_ZTSSt13_Ios_Fmtflags"} ; [ DW_TAG_reference_type ] [line 0, size 0, align 0, offset 0] [from _ZTSSt13_Ios_Fmtflags]
!155 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"operator|", metadata !"operator|", metadata !"_ZStorSt13_Ios_FmtflagsS_", i32 87, metadata !147, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32, i32)* @_ZStorSt13_Ios
!156 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"operator~", metadata !"operator~", metadata !"_ZStcoSt13_Ios_Fmtflags", i32 95, metadata !157, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32 (i32)* @_ZStcoSt13_Ios_Fmtfla
!157 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !158, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!158 = metadata !{metadata !18, metadata !18}
!159 = metadata !{i32 786478, metadata !19, metadata !5, metadata !"operator&=", metadata !"operator&=", metadata !"_ZStaNRSt13_Ios_FmtflagsS_", i32 103, metadata !150, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 false, i32* (i32*, i32)* @_ZStaNRS
!160 = metadata !{i32 786478, metadata !1, metadata !120, metadata !"", metadata !"", metadata !"_GLOBAL__I_a", i32 104, metadata !161, i1 true, i1 true, i32 0, i32 0, null, i32 64, i1 false, void ()* @_GLOBAL__I_a, null, null, metadata !118, i32 104} ; 
!161 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !118, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!162 = metadata !{metadata !163, metadata !164, metadata !166, metadata !168}
!163 = metadata !{i32 786484, i32 0, metadata !5, metadata !"__ioinit", metadata !"__ioinit", metadata !"_ZStL8__ioinit", metadata !115, i32 74, metadata !54, i32 1, i32 1, %"class.std::ios_base::Init"* @_ZStL8__ioinit, null} ; [ DW_TAG_variable ] [__ioi
!164 = metadata !{i32 786484, i32 0, metadata !165, metadata !"digits10", metadata !"digits10", metadata !"digits10", metadata !165, i32 1009, metadata !71, i32 1, i32 1, i32 9, metadata !72} ; [ DW_TAG_variable ] [digits10] [line 1009] [local] [def]
!165 = metadata !{i32 786473, metadata !4}        ; [ DW_TAG_file_type ] [/home/walker/Projects/Experiment/1/case/float_extension//usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/limits]
!166 = metadata !{i32 786484, i32 0, metadata !167, metadata !"scientific", metadata !"scientific", metadata !"scientific", metadata !167, i32 354, metadata !46, i32 1, i32 1, i32 256, metadata !45} ; [ DW_TAG_variable ] [scientific] [line 354] [local] [
!167 = metadata !{i32 786473, metadata !19}       ; [ DW_TAG_file_type ] [/home/walker/Projects/Experiment/1/case/float_extension//usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/ios_base.h]
!168 = metadata !{i32 786484, i32 0, metadata !167, metadata !"floatfield", metadata !"floatfield", metadata !"floatfield", metadata !167, i32 384, metadata !46, i32 1, i32 1, i32 260, metadata !48} ; [ DW_TAG_variable ] [floatfield] [line 384] [local] [
!169 = metadata !{metadata !170, metadata !174}
!170 = metadata !{i32 786490, metadata !171, metadata !173, i32 56} ; [ DW_TAG_imported_module ]
!171 = metadata !{i32 786489, metadata !172, null, metadata !"__gnu_debug", i32 54} ; [ DW_TAG_namespace ] [__gnu_debug] [line 54]
!172 = metadata !{metadata !"/usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/debug/debug.h", metadata !"/home/walker/Projects/Experiment/1/case/float_extension"}
!173 = metadata !{i32 786489, metadata !172, metadata !5, metadata !"__debug", i32 48} ; [ DW_TAG_namespace ] [__debug] [line 48]
!174 = metadata !{i32 786490, metadata !0, metadata !5, i32 12} ; [ DW_TAG_imported_module ]
!175 = metadata !{i32 786449, metadata !176, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !177, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!176 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/klee_div_zero_check.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!177 = metadata !{metadata !178}
!178 = metadata !{i32 786478, metadata !176, metadata !179, metadata !"klee_div_zero_check", metadata !"klee_div_zero_check", metadata !"", i32 12, metadata !180, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, void (i64)* @klee_div_zero_check, 
!179 = metadata !{i32 786473, metadata !176}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_div_zero_check.c]
!180 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !181, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!181 = metadata !{null, metadata !182}
!182 = metadata !{i32 786468, null, null, metadata !"long long int", i32 0, i64 64, i64 64, i64 0, i32 0, i32 5} ; [ DW_TAG_base_type ] [long long int] [line 0, size 64, align 64, offset 0, enc DW_ATE_signed]
!183 = metadata !{metadata !184}
!184 = metadata !{i32 786689, metadata !178, metadata !"z", metadata !179, i32 16777228, metadata !182, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [z] [line 12]
!185 = metadata !{i32 786449, metadata !186, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !187, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!186 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/klee_int.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!187 = metadata !{metadata !188}
!188 = metadata !{i32 786478, metadata !186, metadata !189, metadata !"klee_int", metadata !"klee_int", metadata !"", i32 13, metadata !190, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i32 (i8*)* @klee_int, null, null, metadata !192, i32 13}
!189 = metadata !{i32 786473, metadata !186}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_int.c]
!190 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !191, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!191 = metadata !{metadata !58, metadata !133}
!192 = metadata !{metadata !193, metadata !194}
!193 = metadata !{i32 786689, metadata !188, metadata !"name", metadata !189, i32 16777229, metadata !133, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [name] [line 13]
!194 = metadata !{i32 786688, metadata !188, metadata !"x", metadata !189, i32 14, metadata !58, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [x] [line 14]
!195 = metadata !{i32 786449, metadata !196, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !197, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!196 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/klee_overshift_check.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!197 = metadata !{metadata !198}
!198 = metadata !{i32 786478, metadata !196, metadata !199, metadata !"klee_overshift_check", metadata !"klee_overshift_check", metadata !"", i32 20, metadata !200, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, void (i64, i64)* @klee_overshift
!199 = metadata !{i32 786473, metadata !196}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_overshift_check.c]
!200 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !201, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!201 = metadata !{null, metadata !202, metadata !202}
!202 = metadata !{i32 786468, null, null, metadata !"long long unsigned int", i32 0, i64 64, i64 64, i64 0, i32 0, i32 7} ; [ DW_TAG_base_type ] [long long unsigned int] [line 0, size 64, align 64, offset 0, enc DW_ATE_unsigned]
!203 = metadata !{metadata !204, metadata !205}
!204 = metadata !{i32 786689, metadata !198, metadata !"bitWidth", metadata !199, i32 16777236, metadata !202, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [bitWidth] [line 20]
!205 = metadata !{i32 786689, metadata !198, metadata !"shift", metadata !199, i32 33554452, metadata !202, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [shift] [line 20]
!206 = metadata !{i32 786449, metadata !207, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !208, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!207 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/klee_range.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!208 = metadata !{metadata !209}
!209 = metadata !{i32 786478, metadata !207, metadata !210, metadata !"klee_range", metadata !"klee_range", metadata !"", i32 13, metadata !211, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i32 (i32, i32, i8*)* @klee_range, null, null, metada
!210 = metadata !{i32 786473, metadata !207}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!211 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !212, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!212 = metadata !{metadata !58, metadata !58, metadata !58, metadata !133}
!213 = metadata !{metadata !214, metadata !215, metadata !216, metadata !217}
!214 = metadata !{i32 786689, metadata !209, metadata !"start", metadata !210, i32 16777229, metadata !58, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [start] [line 13]
!215 = metadata !{i32 786689, metadata !209, metadata !"end", metadata !210, i32 33554445, metadata !58, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [end] [line 13]
!216 = metadata !{i32 786689, metadata !209, metadata !"name", metadata !210, i32 50331661, metadata !133, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [name] [line 13]
!217 = metadata !{i32 786688, metadata !209, metadata !"x", metadata !210, i32 14, metadata !58, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [x] [line 14]
!218 = metadata !{i32 786449, metadata !219, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !220, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!219 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/memcpy.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!220 = metadata !{metadata !221}
!221 = metadata !{i32 786478, metadata !219, metadata !222, metadata !"memcpy", metadata !"memcpy", metadata !"", i32 12, metadata !223, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i8* (i8*, i8*, i64)* @memcpy, null, null, metadata !230, i32
!222 = metadata !{i32 786473, metadata !219}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memcpy.c]
!223 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !224, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!224 = metadata !{metadata !225, metadata !225, metadata !226, metadata !228}
!225 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 0, null} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [from ]
!226 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 0, metadata !227} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [from ]
!227 = metadata !{i32 786470, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null} ; [ DW_TAG_const_type ] [line 0, size 0, align 0, offset 0] [from ]
!228 = metadata !{i32 786454, metadata !219, null, metadata !"size_t", i32 42, i64 0, i64 0, i64 0, i32 0, metadata !229} ; [ DW_TAG_typedef ] [size_t] [line 42, size 0, align 0, offset 0] [from long unsigned int]
!229 = metadata !{i32 786468, null, null, metadata !"long unsigned int", i32 0, i64 64, i64 64, i64 0, i32 0, i32 7} ; [ DW_TAG_base_type ] [long unsigned int] [line 0, size 64, align 64, offset 0, enc DW_ATE_unsigned]
!230 = metadata !{metadata !231, metadata !232, metadata !233, metadata !234, metadata !236}
!231 = metadata !{i32 786689, metadata !221, metadata !"destaddr", metadata !222, i32 16777228, metadata !225, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [destaddr] [line 12]
!232 = metadata !{i32 786689, metadata !221, metadata !"srcaddr", metadata !222, i32 33554444, metadata !226, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [srcaddr] [line 12]
!233 = metadata !{i32 786689, metadata !221, metadata !"len", metadata !222, i32 50331660, metadata !228, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [len] [line 12]
!234 = metadata !{i32 786688, metadata !221, metadata !"dest", metadata !222, i32 13, metadata !235, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [dest] [line 13]
!235 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 0, metadata !135} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [from char]
!236 = metadata !{i32 786688, metadata !221, metadata !"src", metadata !222, i32 14, metadata !133, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [src] [line 14]
!237 = metadata !{i32 786449, metadata !238, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !239, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!238 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/memmove.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!239 = metadata !{metadata !240}
!240 = metadata !{i32 786478, metadata !238, metadata !241, metadata !"memmove", metadata !"memmove", metadata !"", i32 12, metadata !242, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i8* (i8*, i8*, i64)* @memmove, null, null, metadata !245, 
!241 = metadata !{i32 786473, metadata !238}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memmove.c]
!242 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !243, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!243 = metadata !{metadata !225, metadata !225, metadata !226, metadata !244}
!244 = metadata !{i32 786454, metadata !238, null, metadata !"size_t", i32 42, i64 0, i64 0, i64 0, i32 0, metadata !229} ; [ DW_TAG_typedef ] [size_t] [line 42, size 0, align 0, offset 0] [from long unsigned int]
!245 = metadata !{metadata !246, metadata !247, metadata !248, metadata !249, metadata !250}
!246 = metadata !{i32 786689, metadata !240, metadata !"dst", metadata !241, i32 16777228, metadata !225, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [dst] [line 12]
!247 = metadata !{i32 786689, metadata !240, metadata !"src", metadata !241, i32 33554444, metadata !226, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [src] [line 12]
!248 = metadata !{i32 786689, metadata !240, metadata !"count", metadata !241, i32 50331660, metadata !244, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [count] [line 12]
!249 = metadata !{i32 786688, metadata !240, metadata !"a", metadata !241, i32 13, metadata !235, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [a] [line 13]
!250 = metadata !{i32 786688, metadata !240, metadata !"b", metadata !241, i32 14, metadata !133, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [b] [line 14]
!251 = metadata !{i32 786449, metadata !252, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !253, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!252 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/mempcpy.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!253 = metadata !{metadata !254}
!254 = metadata !{i32 786478, metadata !252, metadata !255, metadata !"mempcpy", metadata !"mempcpy", metadata !"", i32 11, metadata !256, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i8* (i8*, i8*, i64)* @mempcpy, null, null, metadata !259, 
!255 = metadata !{i32 786473, metadata !252}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/mempcpy.c]
!256 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !257, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!257 = metadata !{metadata !225, metadata !225, metadata !226, metadata !258}
!258 = metadata !{i32 786454, metadata !252, null, metadata !"size_t", i32 42, i64 0, i64 0, i64 0, i32 0, metadata !229} ; [ DW_TAG_typedef ] [size_t] [line 42, size 0, align 0, offset 0] [from long unsigned int]
!259 = metadata !{metadata !260, metadata !261, metadata !262, metadata !263, metadata !264}
!260 = metadata !{i32 786689, metadata !254, metadata !"destaddr", metadata !255, i32 16777227, metadata !225, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [destaddr] [line 11]
!261 = metadata !{i32 786689, metadata !254, metadata !"srcaddr", metadata !255, i32 33554443, metadata !226, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [srcaddr] [line 11]
!262 = metadata !{i32 786689, metadata !254, metadata !"len", metadata !255, i32 50331659, metadata !258, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [len] [line 11]
!263 = metadata !{i32 786688, metadata !254, metadata !"dest", metadata !255, i32 12, metadata !235, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [dest] [line 12]
!264 = metadata !{i32 786688, metadata !254, metadata !"src", metadata !255, i32 13, metadata !133, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [src] [line 13]
!265 = metadata !{i32 786449, metadata !266, i32 1, metadata !"clang version 3.4 (tags/RELEASE_34/final)", i1 true, metadata !"", i32 0, metadata !118, metadata !118, metadata !267, metadata !118, metadata !118, metadata !""} ; [ DW_TAG_compile_unit ] [/
!266 = metadata !{metadata !"/home/walker/Projects/klee/runtime/Intrinsic/memset.c", metadata !"/home/walker/Projects/build_klee_dir/runtime/Intrinsic"}
!267 = metadata !{metadata !268}
!268 = metadata !{i32 786478, metadata !266, metadata !269, metadata !"memset", metadata !"memset", metadata !"", i32 11, metadata !270, i1 false, i1 true, i32 0, i32 0, null, i32 256, i1 true, i8* (i8*, i32, i64)* @memset, null, null, metadata !273, i32
!269 = metadata !{i32 786473, metadata !266}      ; [ DW_TAG_file_type ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memset.c]
!270 = metadata !{i32 786453, i32 0, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, null, metadata !271, i32 0, null, null, null} ; [ DW_TAG_subroutine_type ] [line 0, size 0, align 0, offset 0] [from ]
!271 = metadata !{metadata !225, metadata !225, metadata !58, metadata !272}
!272 = metadata !{i32 786454, metadata !266, null, metadata !"size_t", i32 42, i64 0, i64 0, i64 0, i32 0, metadata !229} ; [ DW_TAG_typedef ] [size_t] [line 42, size 0, align 0, offset 0] [from long unsigned int]
!273 = metadata !{metadata !274, metadata !275, metadata !276, metadata !277}
!274 = metadata !{i32 786689, metadata !268, metadata !"dst", metadata !269, i32 16777227, metadata !225, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [dst] [line 11]
!275 = metadata !{i32 786689, metadata !268, metadata !"s", metadata !269, i32 33554443, metadata !58, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [s] [line 11]
!276 = metadata !{i32 786689, metadata !268, metadata !"count", metadata !269, i32 50331659, metadata !272, i32 0, i32 0} ; [ DW_TAG_arg_variable ] [count] [line 11]
!277 = metadata !{i32 786688, metadata !268, metadata !"a", metadata !269, i32 12, metadata !278, i32 0, i32 0} ; [ DW_TAG_auto_variable ] [a] [line 12]
!278 = metadata !{i32 786447, null, null, metadata !"", i32 0, i64 64, i64 64, i64 0, i32 0, metadata !279} ; [ DW_TAG_pointer_type ] [line 0, size 64, align 64, offset 0] [from ]
!279 = metadata !{i32 786485, null, null, metadata !"", i32 0, i64 0, i64 0, i64 0, i32 0, metadata !135} ; [ DW_TAG_volatile_type ] [line 0, size 0, align 0, offset 0] [from char]
!280 = metadata !{i32 2, metadata !"Dwarf Version", i32 4}
!281 = metadata !{i32 1, metadata !"Debug Info Version", i32 1}
!282 = metadata !{metadata !"clang version 3.4 (tags/RELEASE_34/final)"}
!283 = metadata !{i32 74, i32 0, metadata !113, null}
!284 = metadata !{i32 9, i32 0, metadata !285, null}
!285 = metadata !{i32 786443, metadata !1, metadata !119} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/Experiment/1/case/float_extension/float_extension_i.cc]
!286 = metadata !{i32 16, i32 0, metadata !123, null}
!287 = metadata !{i32 17, i32 0, metadata !288, null}
!288 = metadata !{i32 786443, metadata !1, metadata !123, i32 17, i32 0, i32 0} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/Experiment/1/case/float_extension/float_extension_i.cc]
!289 = metadata !{i32 18, i32 0, metadata !123, null}
!290 = metadata !{i32 22, i32 0, metadata !127, null}
!291 = metadata !{i32 23, i32 0, metadata !127, null}
!292 = metadata !{i32 24, i32 0, metadata !127, null}
!293 = metadata !{i32 25, i32 0, metadata !127, null}
!294 = metadata !{i32 26, i32 0, metadata !127, null}
!295 = metadata !{i32 26, i32 27, metadata !127, null}
!296 = metadata !{i32 26, i32 5, metadata !127, null}
!297 = metadata !{i32 27, i32 0, metadata !127, null}
!298 = metadata !{i32 3, i32 0, metadata !299, null}
!299 = metadata !{i32 786443, metadata !129, metadata !128} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/Experiment/1/case/float_extension//home/walker/Projects/klee/include/klee/klee-expression.h]
!300 = metadata !{i32 1051, i32 0, metadata !301, null}
!301 = metadata !{i32 786443, metadata !19, metadata !141} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/Experiment/1/case/float_extension//usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/ios_base.h]
!302 = metadata !{i32 1052, i32 0, metadata !301, null}
!303 = metadata !{i32 196, i32 0, metadata !304, null}
!304 = metadata !{i32 786443, metadata !109, metadata !138} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/Experiment/1/case/float_extension//usr/lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/iomanip]
!305 = metadata !{i32 665, i32 0, metadata !145, null}
!306 = metadata !{i32 666, i32 0, metadata !145, null}
!307 = metadata !{i32 666, i32 19, metadata !145, null}
!308 = metadata !{i32 666, i32 7, metadata !145, null}
!309 = metadata !{i32 667, i32 0, metadata !145, null}
!310 = metadata !{i32 667, i32 20, metadata !145, null}
!311 = metadata !{i32 667, i32 7, metadata !145, null}
!312 = metadata !{i32 668, i32 0, metadata !145, null}
!313 = metadata !{i32 104, i32 18, metadata !159, null}
!314 = metadata !{i32 96, i32 0, metadata !156, null}
!315 = metadata !{i32 100, i32 18, metadata !149, null}
!316 = metadata !{i32 84, i32 0, metadata !146, null}
!317 = metadata !{i32 88, i32 0, metadata !155, null}
!318 = metadata !{i32 104, i32 0, metadata !160, null}
!319 = metadata !{i32 13, i32 0, metadata !320, null}
!320 = metadata !{i32 786443, metadata !176, metadata !178, i32 13, i32 0, i32 0} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_div_zero_check.c]
!321 = metadata !{i32 14, i32 0, metadata !320, null}
!322 = metadata !{i32 15, i32 0, metadata !178, null}
!323 = metadata !{i32 15, i32 0, metadata !188, null}
!324 = metadata !{i32 16, i32 0, metadata !188, null}
!325 = metadata !{metadata !326, metadata !326, i64 0}
!326 = metadata !{metadata !"int", metadata !327, i64 0}
!327 = metadata !{metadata !"omnipotent char", metadata !328, i64 0}
!328 = metadata !{metadata !"Simple C/C++ TBAA"}
!329 = metadata !{i32 21, i32 0, metadata !330, null}
!330 = metadata !{i32 786443, metadata !196, metadata !198, i32 21, i32 0, i32 0} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_overshift_check.c]
!331 = metadata !{i32 27, i32 0, metadata !332, null}
!332 = metadata !{i32 786443, metadata !196, metadata !330, i32 21, i32 0, i32 1} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_overshift_check.c]
!333 = metadata !{i32 29, i32 0, metadata !198, null}
!334 = metadata !{i32 16, i32 0, metadata !335, null}
!335 = metadata !{i32 786443, metadata !207, metadata !209, i32 16, i32 0, i32 0} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!336 = metadata !{i32 17, i32 0, metadata !335, null}
!337 = metadata !{i32 19, i32 0, metadata !338, null}
!338 = metadata !{i32 786443, metadata !207, metadata !209, i32 19, i32 0, i32 1} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!339 = metadata !{i32 22, i32 0, metadata !340, null}
!340 = metadata !{i32 786443, metadata !207, metadata !338, i32 21, i32 0, i32 3} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!341 = metadata !{i32 25, i32 0, metadata !342, null}
!342 = metadata !{i32 786443, metadata !207, metadata !340, i32 25, i32 0, i32 4} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!343 = metadata !{i32 26, i32 0, metadata !344, null}
!344 = metadata !{i32 786443, metadata !207, metadata !342, i32 25, i32 0, i32 5} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!345 = metadata !{i32 27, i32 0, metadata !344, null}
!346 = metadata !{i32 28, i32 0, metadata !347, null}
!347 = metadata !{i32 786443, metadata !207, metadata !342, i32 27, i32 0, i32 6} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/klee_range.c]
!348 = metadata !{i32 29, i32 0, metadata !347, null}
!349 = metadata !{i32 32, i32 0, metadata !340, null}
!350 = metadata !{i32 34, i32 0, metadata !209, null}
!351 = metadata !{i32 16, i32 0, metadata !221, null}
!352 = metadata !{i32 17, i32 0, metadata !221, null}
!353 = metadata !{metadata !353, metadata !354, metadata !355}
!354 = metadata !{metadata !"llvm.vectorizer.width", i32 1}
!355 = metadata !{metadata !"llvm.vectorizer.unroll", i32 1}
!356 = metadata !{metadata !327, metadata !327, i64 0}
!357 = metadata !{metadata !357, metadata !354, metadata !355}
!358 = metadata !{i32 18, i32 0, metadata !221, null}
!359 = metadata !{i32 16, i32 0, metadata !360, null}
!360 = metadata !{i32 786443, metadata !238, metadata !240, i32 16, i32 0, i32 0} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memmove.c]
!361 = metadata !{i32 19, i32 0, metadata !362, null}
!362 = metadata !{i32 786443, metadata !238, metadata !240, i32 19, i32 0, i32 1} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memmove.c]
!363 = metadata !{i32 20, i32 0, metadata !364, null}
!364 = metadata !{i32 786443, metadata !238, metadata !362, i32 19, i32 0, i32 2} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memmove.c]
!365 = metadata !{metadata !365, metadata !354, metadata !355}
!366 = metadata !{metadata !366, metadata !354, metadata !355}
!367 = metadata !{i32 22, i32 0, metadata !368, null}
!368 = metadata !{i32 786443, metadata !238, metadata !362, i32 21, i32 0, i32 3} ; [ DW_TAG_lexical_block ] [/home/walker/Projects/build_klee_dir/runtime/Intrinsic//home/walker/Projects/klee/runtime/Intrinsic/memmove.c]
!369 = metadata !{i32 24, i32 0, metadata !368, null}
!370 = metadata !{i32 23, i32 0, metadata !368, null}
!371 = metadata !{metadata !371, metadata !354, metadata !355}
!372 = metadata !{metadata !372, metadata !354, metadata !355}
!373 = metadata !{i32 28, i32 0, metadata !240, null}
!374 = metadata !{i32 15, i32 0, metadata !254, null}
!375 = metadata !{i32 16, i32 0, metadata !254, null}
!376 = metadata !{metadata !376, metadata !354, metadata !355}
!377 = metadata !{metadata !377, metadata !354, metadata !355}
!378 = metadata !{i32 17, i32 0, metadata !254, null}
!379 = metadata !{i32 13, i32 0, metadata !268, null}
!380 = metadata !{i32 14, i32 0, metadata !268, null}
!381 = metadata !{i32 15, i32 0, metadata !268, null}

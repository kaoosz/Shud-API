<?php

namespace App\Http\Resources;

use Illuminate\Support\Str;




use Illuminate\Http\Resources\Json\JsonResource;



class CandidateResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {
        return [

            'NM_CANDIDATO' => $this->NM_CANDIDATO,
            'NM_URNA_CANDIDATO' => $this->NM_URNA_CANDIDATO,
            'NR_CPF_CANDIDATO' => $this->when(Str::length($this->NR_CPF_CANDIDATO) < 11,function(){
                return '0'.$this->NR_CPF_CANDIDATO;
            },$this->NR_CPF_CANDIDATO),
            'SG_UF' => $this->SG_UF,
            'NM_UE' => $this->NM_UE,
            'DS_CARGO' => $this->DS_CARGO,
            'ANO_ELEICAO' => $this->ANO_ELEICAO,
            'NR_CANDIDATO' => $this->NR_CANDIDATO,
            'CD_ELEICAO' => $this->CD_ELEICAO,
            'votos_escola' => $this->when($request->get('escola'),function() use($request){
                if($request->get('UF') and $request->get('escola')){
                    return $this->whenLoaded($request->get('escola'))->where("NM_MUNICIPIO", request()->get('UF'))->sum('QT_VOTOS');
                }
                return $this->whenLoaded($request->get('escola'))->sum('QT_VOTOS');
            }),
            'votos_bairro' => $this->when($request->get('bairro'),function() use($request){
                if($request->get('UF') and $request->get('bairro')){
                    return $this->whenLoaded($request->get('bairro'))->where("NM_MUNICIPIO", request()->get('UF'))->sum('QT_VOTOS');
                }
                return $this->whenLoaded($request->get('bairro'))->sum('QT_VOTOS');
            }),
            'votos_cidade' => $this->when($request->get('cidade'),function() use($request){
                if($request->get('UF') and $request->get('cidade')){
                    return $this->whenLoaded($request->get('cidade'))->where("NM_MUNICIPIO", request()->get('UF'))->sum('QT_VOTOS');
                }
                return $this->whenLoaded($request->get('cidade'))->sum('QT_VOTOS');
            }),

            // BAIRRO

            'bairro2020' => $this->when($request->get('bairro') === 'bairro2020',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->bairro2020()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->bairro2020()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->bairro2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->bairro2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'bairro2018' => $this->when($request->get('bairro') === 'bairro2018',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->bairro2018()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->bairro2018()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->bairro2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->bairro2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'bairro2016' => $this->when($request->get('bairro') === 'bairro2016',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->bairro2016()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->bairro2016()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->bairro2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->bairro2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'bairro2014' => $this->when($request->get('bairro') === 'bairro2014',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->bairro2014()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->bairro2014()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->bairro2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->bairro2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'bairro2012' => $this->when($request->get('bairro') === 'bairro2012',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->bairro2012()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->bairro2012()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->bairro2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->bairro2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),

            ///////////////////////////////////////////////////
            // ESCOLAS
            'schools2020' => $this->when($request->get('escola') === 'schools2020',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->schools2020()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->has('paginate')){
                    return $this->schools2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->schools2020()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }
                return $this->schools2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'schools2018' => $this->when($request->get('escola') === 'schools2018',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->schools2018()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->has('paginate')){
                    return $this->schools2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->schools2018()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }
                return $this->schools2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'schools2016' => $this->when($request->get('escola') === 'schools2016',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->schools2016()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->has('paginate')){
                    return $this->schools2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->schools2016()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }
                return $this->schools2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'schools2014' => $this->when($request->get('escola') === 'schools2014',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->schools2014()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->has('paginate')){
                    return $this->schools2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->schools2014()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }
                return $this->schools2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'schools2012' => $this->when($request->get('escola') === 'schools2012',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->schools2012()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->has('paginate')){
                    return $this->schools2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->schools2012()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }
                return $this->schools2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),

            // CITIES
            // CIDADES
            'cities2020' => $this->when($request->get('cidade') === 'cities2020',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->cities2020()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->cities2020()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->cities2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->cities2020()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'cities2018' => $this->when($request->get('cidade') === 'cities2018',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->cities2018()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->cities2018()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->cities2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->cities2018()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'cities2016' => $this->when($request->get('cidade') === 'cities2016',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->cities2016()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->cities2016()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->cities2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->cities2016()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'cities2014' => $this->when($request->get('cidade') === 'cities2014',function() use($request){
                if($request->has('paginate') and $request->get('UF')){

                    return $this->cities2014()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->cities2014()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->cities2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->cities2014()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),
            'cities2012' => $this->when($request->get('cidade') === 'cities2012',function() use($request){
                if($request->has('paginate') and $request->get('UF')){
                    return $this->cities2012()->where("NM_MUNICIPIO", request()->get('UF'))->paginate()->withQueryString();
                }else if($request->get('UF')){
                    return $this->cities2012()->where("NM_MUNICIPIO", request()->get('UF'))->get();
                }else if($request->has('paginate')){
                    return $this->cities2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->paginate()->withQueryString();
                }
                return $this->cities2012()->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'))->get();
            }),


        ];


    }





}

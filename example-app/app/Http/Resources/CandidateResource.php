<?php

namespace App\Http\Resources;

use App\Models\Candidate;
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
            'NR_CPF_CANDIDATO' => $this->NR_CPF_CANDIDATO,
            'SG_UF' => $this->SG_UF,
            'NM_UE' => $this->NM_UE,
            'DS_CARGO' => $this->DS_CARGO,
            'ANO_ELEICAO' => $this->ANO_ELEICAO,
            'NR_CANDIDATO' => $this->NR_CANDIDATO,
            'CD_ELEICAO' => $this->CD_ELEICAO,
            //'CD_ELEICAO' => $this->when($request->get('show') === 'all', $this->CD_ELEICAO),
            //'votesneighborhood' => $this->whenLoaded('votesneighborhood'),


            'votesneighborhood' => $this->when($request->get('bairro') === 'votesneighborhood',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'votesneighborhood'){
                    return $this->whenLoaded('votesneighborhood')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('votesneighborhood')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'bairro2018' => $this->when($request->get('bairro') === 'bairro2018',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'bairro2018'){
                    return $this->whenLoaded('bairro2018')->where("NM_MUNICIPIO", request()->get('UF'));//akui
                }else{
                    return $this->whenLoaded('bairro2018');
                }
            }),
            'bairro2016' => $this->when($request->get('bairro') === 'bairro2016',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'bairro2016'){
                    return $this->whenLoaded('bairro2016')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('bairro2016');
                }
            }),
            'bairro2014' => $this->when($request->get('bairro') === 'bairro2014',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'bairro2014'){
                    return $this->whenLoaded('bairro2014')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('bairro2014');
                }
            }),
            'bairro2012' => $this->when($request->get('bairro') === 'bairro2012',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'bairro2012'){
                    return $this->whenLoaded('bairro2012')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('bairro2012');
                }
            }),
            ///////////////////////////////////////////////////

            // 'schools2018' => $this->when($request->get('ANO') === '2018' ,function(){
            //     return $this->whenLoaded('schools2018');
            // }),
            'schools2020' => $this->when($request->get('escola') === 'schools2020',function() use($request){
                if($request->get('UF') and $request->get('escola') === 'schools2020'){
                    return $this->whenLoaded('schools2020')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('schools2020')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'schools2018' => $this->when($request->get('escola') === 'schools2018',function() use($request){
                if($request->get('UF') and $request->get('escola') === 'schools2018'){
                    return $this->whenLoaded('schools2018')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('schools2018')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'schools2016' => $this->when($request->get('escola') === 'schools2016',function() use($request){
                if($request->get('UF') and $request->get('escola') === 'schools2016'){
                    return $this->whenLoaded('schools2016')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('schools2016')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'schools2014' => $this->when($request->get('escola') === 'schools2014',function() use($request){
                if($request->get('UF') and $request->get('escola') === 'schools2014'){
                    return $this->whenLoaded('schools2014')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('schools2014')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'schools2012' => $this->when($request->get('escola') === 'schools2012',function() use($request){
                if($request->get('UF') and $request->get('escola') === 'schools2012'){
                    return $this->whenLoaded('schools2012')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('schools2012')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),

            // CITIES
            // CITIES

            'cities2020' => $this->when($request->get('cidade') === 'cities2020',function() use($request){
                if($request->get('UF') and $request->get('cidade') === 'cities2020'){
                    return $this->whenLoaded('cities2020')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('cities2020')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'cities2018' => $this->when($request->get('cidade') === 'cities2018',function() use($request){
                if($request->get('UF') and $request->get('cidade') === 'cities2018'){
                    return $this->whenLoaded('cities2018')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('cities2018')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'cities2016' => $this->when($request->get('cidade') === 'cities2016',function() use($request){
                if($request->get('UF') and $request->get('cidade') === 'cities2016'){
                    return $this->whenLoaded('cities2016')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('cities2016')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'cities2014' => $this->when($request->get('cidade') === 'cities2014',function() use($request){
                if($request->get('UF') and $request->get('cidade') === 'cities2014'){
                    return $this->whenLoaded('cities2014')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('cities2014')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),
            'cities2012' => $this->when($request->get('cidade') === 'cities2012',function() use($request){
                if($request->get('UF') and $request->get('cidade') === 'cities2012'){
                    return $this->whenLoaded('cities2012')->where("NM_MUNICIPIO", request()->get('UF'));
                }else{
                    return $this->whenLoaded('cities2012')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
                }
            }),




            // 'schools2012' => $this->when($request->get('ANO') === '2012',function() use($request){
            //     if($request->get('UF')){
            //         return $this->whenLoaded('schools2012')->where("NM_MUNICIPIO", request()->get('UF'));
            //     }else{
            //         return $this->whenLoaded('schools2012')->where("NR_VOTAVEL", request()->get('NR_CANDIDATO'));
            //     }
            // }),

            ///////////////////////////
            //'schools2020' => $this->whenLoaded('schools2020'),

            //////////////////////////////////////////////////////
            // 'schools2020' => $this->when($request->get('bairro') === 'schools2020',function() use($request){
            //     if($request->get('UF') and $request->get('bairro') === 'schools2020'){
            //         return $this->whenLoaded('schools2020')->where("NM_MUNICIPIO", request()->get('UF'));
            //     }else{
            //         return $this->whenLoaded('schools2020');
            //     }
            // }),
        ];

    }
}
